import streamlit as st
import requests
import json

API_BASE = "http://localhost:5000"

st.title("Placement Dashboard — Resume Relevance")

st.sidebar.header("Upload Job Description")
with st.sidebar.form("jd_form"):
    jd_file = st.file_uploader("Upload JD (txt/pdf/docx)", type=["txt", "pdf", "docx"])
    jd_id = st.text_input("JD ID", value="jd1")
    must = st.text_input("Must skills (comma-separated)", "")
    nice = st.text_input("Nice skills (comma-separated)", "")
    submitted = st.form_submit_button("Upload JD")
    if submitted and jd_file:
        files = {"file": (jd_file.name, jd_file.read())}
        data = {"jd_id": jd_id, "must_skills": must, "nice_skills": nice}
        resp = requests.post(f"{API_BASE}/upload_jd/", files=files, data=data)
        try:
            response_data = resp.json()
            print(response_data)
            st.write(response_data)
        except json.JSONDecodeError:
            st.error(f"Error: Invalid response format. Status code: {resp.status_code}")


st.header("Upload Resume to Evaluate")
resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
resume_id = st.text_input("Resume ID", value="r1")
jd_choice = st.text_input("JD ID to evaluate against", value="jd1")
if st.button("Evaluate"):
    if resume_file:
        files = {"file": (resume_file.name, resume_file.read())}
        data = {"resume_id": resume_id, "jd_id": jd_choice}
        resp = requests.post(f"{API_BASE}/upload_resume/", files=files, data=data)

        try:
            response_data = resp.json()
            # st.write(response_data)
        except json.JSONDecodeError:
            st.error(f"Error: Invalid response format. Status code: {resp.status_code}")

        result = response_data.get("result", None)
        hard_score = result.get("hard_score", None)
        score = result.get("score", None)
        semantic_score = result.get("semantic_score", None)
        verdict = result.get("verdict", None)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Hard Score")
            st.metric(
                label="Hard Score",
                value=hard_score if hard_score is not None else "N/A",
            )

        with col2:
            st.subheader("Semantic Score")
            st.metric(
                label="Semantic Score",
                value=semantic_score if semantic_score is not None else "N/A",
            )

        with col3:
            st.subheader("Total Score")
            st.metric(
                label="Total Score",
                value=score if score is not None else "N/A",
            )

        with col4:
            st.subheader("Verdict")
            st.metric(label="Verdict", value=verdict if verdict is not None else "N/A")

        # Optionally, update session_state after evaluation
        if "response_data" in locals() and isinstance(response_data, dict):
            st.session_state["hard_score"] = response_data.get("hard_score")
            st.session_state["soft_score"] = response_data.get("soft_score")
            st.session_state["semantic_score"] = response_data.get("semantic_score")
            st.session_state["verdict"] = response_data.get("verdict")


st.header("Search Evaluations")
rid = st.text_input("Resume ID to view")
if st.button("Get Eval"):
    if rid:
        resp = requests.get(f"{API_BASE}/get_eval/{rid}")
        # data = st.json(resp.json())

        st.header("Evaluation Components")
        
        try:
            result = resp.json()
            # st.write(response_data)
        except json.JSONDecodeError:
            st.error(f"Error: Invalid response format. Status code: {resp.status_code}")

        hard_score = result.get("hard_score", None)
        score = result.get("score", None)
        semantic_score = result.get("semantic_score", None)
        verdict = result.get("verdict", None)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Hard Score")
            st.metric(
                label="Hard Score",
                value=hard_score if hard_score is not None else "N/A",
            )

        with col2:
            st.subheader("Semantic Score")
            st.metric(
                label="Semantic Score",
                value=semantic_score if semantic_score is not None else "N/A",
            )

        with col3:
            st.subheader("Total Score")
            st.metric(
                label="Total Score",
                value=score if score is not None else "N/A",
            )

        with col4:
            st.subheader("Verdict")
            st.metric(label="Verdict", value=verdict if verdict is not None else "N/A")

        # Optionally, update session_state after evaluation
        if "response_data" in locals() and isinstance(response_data, dict):
            st.session_state["hard_score"] = response_data.get("hard_score")
            st.session_state["soft_score"] = response_data.get("soft_score")
            st.session_state["semantic_score"] = response_data.get("semantic_score")
            st.session_state["verdict"] = response_data.get("verdict")
