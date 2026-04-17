# AI Log Analyzer Chatbot

An intelligent log analysis chatbot powered by **Groq API (Llama 3)**, **LangChain**, and **FastAPI** — built to automatically detect log types, tag severity, identify root causes, and suggest fixes in plain English.

---

## What It Does

Developers spend hours manually reading through cryptic error logs. This project solves that by letting you paste any raw system or application log and instantly getting back a structured diagnosis — error type, root cause, exact fix, and follow-up questions to continue debugging.

---

## Features

- **Smart log type detection** — automatically identifies Python tracebacks, database errors, or generic system logs and uses a tailored prompt for each
- **Severity auto-tagging** — classifies every log as Low, Medium, High, or Critical using regex before the LLM is even called
- **Root cause analysis** — powered by Groq's Llama 3 model via LangChain prompt chains
- **Conversation memory** — session-aware chatbot remembers context so follow-up questions work naturally
- **Follow-up question suggestions** — after every analysis the system suggests 2 relevant next questions as clickable buttons
- **Session history sidebar** — last 5 analyzed logs stored in session for quick reference
- **REST API** — fully documented FastAPI backend with Swagger UI at `/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Backend | FastAPI + Python |
| AI Chain | LangChain |
| LLM | Groq API — Llama 3 (70B) |
| Log Processing | Python `re` (regex) |
| Memory | LangChain ConversationBufferMemory |
| Environment | python-dotenv |

---

## System Architecture

```
User (Streamlit UI)
        |
        | pastes raw log
        v
  FastAPI Backend
  POST /analyze
        |
        v
  Preprocessor
  - clean log text
  - tag severity (regex)
        |
        v
  Smart Prompt Builder
  - detect log type (Python / DB / Generic)
  - select tailored prompt template
        |
        v
  LangChain Chain
  - ConversationBufferMemory
  - session-aware context
        |
        v
  Groq API — Llama 3
  - fast LLM inference
        |
        v
  Structured Response
  - Error type
  - Root cause
  - Suggested fix
  - Follow-up questions
        |
        v
  Streamlit UI renders result
  + severity badge + clickable follow-ups
```

---

## Project Structure

```
aichatbot_log/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app + /analyze route
│   ├── myschemas.py             # Pydantic request/response models
│   ├── chains/
│   │   ├── __init__.py
│   │   └── analyzer_chain.py   # LangChain chain + Groq API call
│   ├── core/
│   │   ├── __init__.py
│   │   ├── log_preprocessor.py # Log cleaner + severity tagger
│   │   └── prompt_builder.py   # Log type detector + prompt router
│   └── ui/
│       ├── __init__.py
│       └── streamlit_app.py    # Streamlit chatbot UI
├── .env                         # GROQ_API_KEY goes here
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9 or above
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/aichatbot_log.git
cd aichatbot_log

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
echo GROQ_API_KEY=your_key_here > .env
```

### Running the App

You need **two terminals open simultaneously**.

**Terminal 1 — Start the FastAPI backend:**
```bash
uvicorn app.main:app --reload
```

**Terminal 2 — Start the Streamlit UI:**
```bash
streamlit run app/ui/streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

---

## API Usage

The FastAPI backend is also usable as a standalone REST API.

**Endpoint:** `POST /analyze`

**Request body:**
```json
{
  "log_text": "Traceback (most recent call last):\n  File app.py, line 10\nKeyError: 'user_id'",
  "session_id": "my-session-123"
}
```

**Response:**
```json
{
  "error_type": "KeyError",
  "severity": "High",
  "log_type": "python",
  "root_cause": "The key 'user_id' does not exist in the dictionary being accessed",
  "suggested_fix": "Check if the key exists before accessing it using .get() or an explicit key check",
  "follow_up_questions": [
    "How do I safely access dictionary keys in Python?",
    "How can I prevent this error in future?"
  ],
  "raw_response": "..."
}
```

Visit `http://127.0.0.1:8000/docs` for full interactive API documentation.

---

## Screenshots


### Analysis Result — Python Traceback

> *[ paste your screenshot here ]*


---

## Development Phases

**Phase 1 — Core backend**
FastAPI server, `/analyze` endpoint, LangChain + Groq integration, basic prompt, structured JSON response.

**Phase 2 — Intelligence layer**
Log preprocessor with regex severity tagging, smart prompt builder for log type detection, LangChain conversation memory, follow-up question generation.

**Phase 3 — Streamlit UI**
Chat interface, severity badges, clickable follow-up buttons, session history sidebar, full integration with FastAPI backend.

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

---

## Requirements

```
fastapi
uvicorn
langchain
langchain-groq
langchain-community
python-dotenv
pydantic
streamlit
requests
```

---

## License

MIT License — free to use, modify, and distribute.

---

## Author

Built as a portfolio project demonstrating end-to-end AI backend engineering with FastAPI, LangChain, and Groq LLM integration.
