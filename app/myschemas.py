from pydantic import BaseModel

class LogRequest(BaseModel):
    log_text: str

class LogResponse(BaseModel):
    error_type: str
    severity: str
    root_cause: str
    suggested_fix: str
    raw_response: str