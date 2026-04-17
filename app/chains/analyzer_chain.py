import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import app.core.prompt_builder
from app.core.log_preprocessor import clean_log, tag_severity

load_dotenv()

print("API KEY:", os.getenv("GROQ_API_KEY"))

# -----------------------------------------------
# GROQ API KEY loaded from .env file
# .env must contain: GROQ_API_KEY=your_key_here
# -----------------------------------------------

session_store: dict = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.2
    )

def parse_llm_response(raw: str) -> dict:
    result = {
        "error_type": "Unknown",
        "root_cause": "Unknown",
        "suggested_fix": "Unknown",
        "follow_up_questions": [],
        "raw_response": raw
    }

    for line in raw.strip().splitlines():
        line = line.strip()
        if line.startswith("ERROR TYPE:"):
            result["error_type"] = line.replace("ERROR TYPE:", "").strip()
        elif line.startswith("ROOT CAUSE:"):
            result["root_cause"] = line.replace("ROOT CAUSE:", "").strip()
        elif line.startswith("SUGGESTED FIX:"):
            result["suggested_fix"] = line.replace("SUGGESTED FIX:", "").strip()
        elif line.startswith("FOLLOW UP QUESTIONS:"):
            raw_questions = line.replace("FOLLOW UP QUESTIONS:", "").strip()
            raw_questions = raw_questions.lstrip("|").strip()
            result["follow_up_questions"] = [
                q.strip() for q in raw_questions.split("|") if q.strip()
            ]

    return result

def analyze_log(log_text: str, session_id: str = "default") -> dict:
    cleaned = clean_log(log_text)
    severity = tag_severity(cleaned)
    prompt, log_type = app.core.prompt_builder.get_prompt(cleaned)

    llm = get_llm()
    chain = prompt | llm | StrOutputParser()

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="log_text",
        history_messages_key="history",
    )

    raw_response = chain_with_history.invoke(
        {"log_text": cleaned},
        config={"configurable": {"session_id": session_id}}
    )

    parsed = parse_llm_response(raw_response)
    parsed["severity"] = severity
    parsed["log_type"] = log_type

    return parsed