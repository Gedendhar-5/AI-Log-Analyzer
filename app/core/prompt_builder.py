import re
from langchain_core.prompts import ChatPromptTemplate

PYTHON_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Python debugger.
The user has shared a Python traceback or error log.
Respond in this exact format with no extra text:

ERROR TYPE: <one line>
ROOT CAUSE: <one line>
SUGGESTED FIX: <one to two lines>
FOLLOW UP QUESTIONS: <write exactly 2 questions the user might ask next, separated by | >
"""),
    ("human", "Analyze this Python log:\n\n{log_text}"),
])

DATABASE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert database administrator and debugger.
The user has shared a database error log.
Respond in this exact format with no extra text:

ERROR TYPE: <one line>
ROOT CAUSE: <one line>
SUGGESTED FIX: <one to two lines>
FOLLOW UP QUESTIONS: <write exactly 2 questions the user might ask next, separated by | >
"""),
    ("human", "Analyze this database log:\n\n{log_text}"),
])

GENERIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert software debugger and log analyzer.
The user has shared a system or application log.
Respond in this exact format with no extra text:

ERROR TYPE: <one line>
ROOT CAUSE: <one line>
SUGGESTED FIX: <one to two lines>
FOLLOW UP QUESTIONS: <write exactly 2 questions the user might ask next, separated by | >
"""),
    ("human", "Analyze this log:\n\n{log_text}"),
])

def detect_log_type(log_text: str) -> str:
    log_upper = log_text.upper()

    python_signals = ["TRACEBACK", "KEYERROR", "TYPEERROR", "VALUEERROR",
                      "INDEXERROR", "ATTRIBUTEERROR", "IMPORTERROR",
                      "FILE \"", ".PY\","]
    for signal in python_signals:
        if signal in log_upper:
            return "python"

    db_signals = ["SQL", "MYSQL", "POSTGRESQL", "SQLITE", "ORA-",
                  "DEADLOCK", "SYNTAX ERROR", "TABLE", "QUERY"]
    for signal in db_signals:
        if signal in log_upper:
            return "database"

    return "generic"

def get_prompt(log_text: str) -> tuple:
    log_type = detect_log_type(log_text)

    if log_type == "python":
        return PYTHON_PROMPT, log_type
    elif log_type == "database":
        return DATABASE_PROMPT, log_type
    else:
        return GENERIC_PROMPT, log_type