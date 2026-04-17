import re

def clean_log(log_text: str) -> str:
    log_text = log_text.strip()
    log_text = re.sub(r'\n{3,}', '\n\n', log_text)
    log_text = re.sub(r'[ \t]+', ' ', log_text)
    return log_text

def tag_severity(log_text: str) -> str:
    log_upper = log_text.upper()

    critical_keywords = ["FATAL", "OUT OF MEMORY", "OOM", "SEGFAULT", "KERNEL PANIC", "CRITICAL"]
    high_keywords = ["ERROR", "EXCEPTION", "TRACEBACK", "500", "FAILED", "FAILURE"]
    medium_keywords = ["WARN", "WARNING", "TIMEOUT", "DEPRECATED", "RETRY"]

    for word in critical_keywords:
        if word in log_upper:
            return "Critical"

    for word in high_keywords:
        if word in log_upper:
            return "High"

    for word in medium_keywords:
        if word in log_upper:
            return "Medium"

    return "Low"
