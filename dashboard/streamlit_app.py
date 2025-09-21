import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000"

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
            st.write(response_data)
        except json.JSONDecodeError:
            st.error(f"Error: Invalid response format. Status code: {resp.status_code}")

st.header("Search Evaluations")
rid = st.text_input("Resume ID to view")
if st.button("Get Eval"):
    if rid:
        resp = requests.get(f"{API_BASE}/get_eval/{rid}")
        st.json(resp.json())
