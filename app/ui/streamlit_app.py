import streamlit as st
import requests
import uuid

FASTAPI_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="AI Log Analyzer",
    page_icon="🔍",
    layout="centered"
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

if "follow_up_questions" not in st.session_state:
    st.session_state.follow_up_questions = []

if "pending_log" not in st.session_state:
    st.session_state.pending_log = ""

SEVERITY_COLORS = {
    "Critical": "🔴 Critical",
    "High":     "🟠 High",
    "Medium":   "🟡 Medium",
    "Low":      "🟢 Low"
}

LOG_TYPE_LABELS = {
    "python":   "🐍 Python",
    "database": "🗄️ Database",
    "generic":  "📄 Generic"
}

def call_api(log_text: str, session_id: str) -> dict:
    try:
        response = requests.post(
            FASTAPI_URL,
            json={
                "log_text": log_text
            },
            timeout=30
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            detail = response.json().get("detail", "Unknown error")
            return {"success": False, "error": detail}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Is FastAPI running?"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def display_result(result: dict):
    severity_label = SEVERITY_COLORS.get(result.get("severity", "Low"), "🟢 Low")
    log_type_label = LOG_TYPE_LABELS.get(result.get("log_type", "generic"), "📄 Generic")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Severity:** {severity_label}")
    with col2:
        st.markdown(f"**Log type:** {log_type_label}")

    st.markdown("#### Error type")
    st.info(result.get("error_type", "Unknown"))

    st.markdown("#### Root cause")
    st.warning(result.get("root_cause", "Unknown"))

    st.markdown("#### Suggested fix")
    st.success(result.get("suggested_fix", "Unknown"))

def display_follow_ups(questions: list):
    if not questions:
        return

    st.markdown("---")
    st.markdown("**You might want to ask:**")

    for i, question in enumerate(questions):
        if question.strip():
            if st.button(question.strip(), key=f"followup_{i}_{question[:20]}"):
                st.session_state.pending_log = question.strip()
                st.rerun()

def display_sidebar():
    with st.sidebar:
        st.markdown("## Session history")

        if not st.session_state.history:
            st.markdown("*No logs analyzed yet*")
            return

        st.markdown(f"*{len(st.session_state.history)} log(s) analyzed this session*")
        st.markdown("---")

        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"Log {len(st.session_state.history) - i} — {item['severity']}"):
                st.markdown(f"**Type:** {item['log_type']}")
                st.markdown(f"**Error:** {item['error_type']}")
                st.markdown(f"**Fix:** {item['suggested_fix']}")

        if st.button("Clear history"):
            st.session_state.history = []
            st.session_state.follow_up_questions = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

def main():
    st.title("AI Log Analyzer")
    st.markdown("Paste any system or application log and get an instant AI-powered diagnosis.")

    display_sidebar()

    log_input = st.text_area(
        label="Paste your log here",
        value=st.session_state.pending_log,
        height=200,
        placeholder="Paste your error log, traceback, or system log here...",
        key="log_input"
    )

    if st.session_state.pending_log:
        st.session_state.pending_log = ""

    analyze_clicked = st.button("Analyze log", type="primary", use_container_width=True)

    if analyze_clicked:
        if not log_input.strip():
            st.error("Please paste a log before clicking Analyze.")
        else:
            with st.spinner("Analyzing your log..."):
                result = call_api(log_input.strip(), st.session_state.session_id)

            if not result["success"]:
                st.error(f"Error: {result['error']}")
            else:
                data = result["data"]
                display_result(data)

                follow_ups = data.get("follow_up_questions", [])
                st.session_state.follow_up_questions = follow_ups

                st.session_state.history.append({
                    "log_text": log_input.strip()[:100],
                    "error_type": data.get("error_type", "Unknown"),
                    "severity": data.get("severity", "Low"),
                    "log_type": data.get("log_type", "generic"),
                    "suggested_fix": data.get("suggested_fix", "Unknown")
                })

    if st.session_state.follow_up_questions:
        display_follow_ups(st.session_state.follow_up_questions)

if __name__ == "__main__":
    main()