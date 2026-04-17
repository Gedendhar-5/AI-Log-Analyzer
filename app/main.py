from fastapi import FastAPI, HTTPException
from app.myschemas import LogRequest, LogResponse
from app.chains.analyzer_chain import analyze_log

app = FastAPI(
    title="AI Log Analyzer",
    description="Paste any system log and get instant AI-powered debugging",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI Log Analyzer is running"}

@app.post("/analyze", response_model=LogResponse)
def analyze(request: LogRequest):
    if not request.log_text.strip():
        raise HTTPException(status_code=400, detail="Log text cannot be empty")
    
    if len(request.log_text) > 50000:
        raise HTTPException(status_code=400, detail="Log too large, max 50000 characters")

    try:
        result = analyze_log(request.log_text)
        return LogResponse(
            error_type=result["error_type"],
            severity="High",          # Phase 2 will make this dynamic
            root_cause=result["root_cause"],
            suggested_fix=result["suggested_fix"],
            raw_response=result["raw_response"]
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {str(e)}")