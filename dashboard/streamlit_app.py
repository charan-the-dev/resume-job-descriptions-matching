import streamlit as st
import requests
import json

# Custom CSS for the new UI design
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background-color: #0a0a0a;
        color: #00bcd4;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        color: #00bcd4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    /* Card styling */
    .ui-card {
        background-color: #1a1a1a;
        border: 2px solid #00bcd4;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 188, 212, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #00bcd4;
        color: #000;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #0097a7;
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0a0a0a;
        border-right: 2px solid #00bcd4;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        border: 1px solid #00bcd4;
        color: #00bcd4;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #1a1a1a;
        border: 2px dashed #00bcd4;
    }
    
    /* Score card styling */
    .score-card {
        background-color: #1a1a1a;
        border: 1px solid #00bcd4;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .score-title {
        color: #00bcd4;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .score-value {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Section headers */
    .section-header {
        color: #00bcd4;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# Main header
st.markdown('<div class="main-header">Updated Upload docs UI</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio("", ["Upload Docs", "Past Analysis"], 
                       format_func=lambda x: f"📄 {x}" if x == "Upload Docs" else f"📊 {x}")

# ---------------------------
# UPLOAD DOCS PAGE
# ---------------------------
if page == "Upload Docs":
    # Create three columns layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Upload Docs</div>', unsafe_allow_html=True)
        st.markdown("Past Analysis", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">JDs upload</div>', unsafe_allow_html=True)
        
        with st.form("jd_form"):
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
                    st.success("JD uploaded successfully!")
                    st.json(resp.json())
                except json.JSONDecodeError:
                    st.error(f"Error: Invalid response format. Status code: {resp.status_code}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Resume Upload</div>', unsafe_allow_html=True)
        
        with st.form("resume_form"):
            resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
            resume_id = st.text_input("Resume ID", value="r1")
            jd_choice = st.text_input("JD ID to evaluate against", value="jd1")
            evaluate = st.form_submit_button("Evaluate Resume")
            
            if evaluate and resume_file:
                files = {"file": (resume_file.name, resume_file.read())}
                data = {"resume_id": resume_id, "jd_id": jd_choice}
                resp = requests.post(f"{API_BASE}/upload_resume/", files=files, data=data)
                try:
                    response_data = resp.json()
                    st.success("Resume evaluated successfully!")
                    # Store results in session state to display below
                    st.session_state.evaluation_results = response_data
                except json.JSONDecodeError:
                    st.error(f"Error: Invalid response format. Status code: {resp.status_code}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Score/Result section (full width)
    if 'evaluation_results' in st.session_state:
        st.markdown('<div class="section-header">Score / Result</div>', unsafe_allow_html=True)
        
        # Create scoring grid
        score_col1, score_col2 = st.columns(2)
        
        with score_col1:
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Hard Scoring</div>
                <div class="score-value">{st.session_state.evaluation_results.get("hard_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Verdict</div>
                <div class="score-value">{st.session_state.evaluation_results.get("verdict", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with score_col2:
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Semantic Scoring</div>
                <div class="score-value">{st.session_state.evaluation_results.get("semantic_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Overall Scoring</div>
                <div class="score-value">{st.session_state.evaluation_results.get("overall_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)

# ---------------------------
# PAST ANALYSIS PAGE
# ---------------------------
elif page == "Past Analysis":
    st.markdown('<div class="main-header">Updated Past Analysis UI</div>', unsafe_allow_html=True)
    
    # Create layout similar to the second image
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Upload Docs</div>', unsafe_allow_html=True)
        st.markdown("Past Analysis", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">JD Id</div>', unsafe_allow_html=True)
        jd_id_input = st.text_input("Enter JD ID", key="past_jd_id")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Resume ID</div>', unsafe_allow_html=True)
        resume_id_input = st.text_input("Enter Resume ID", key="past_resume_id")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Search button
    col_center = st.columns([1, 1, 1])[1]
    with col_center:
        search_button = st.button("Get Past Result", key="search_past")
    
    if search_button:
        if jd_id_input and resume_id_input:
            resp = requests.get(f"{API_BASE}/get_eval/{resume_id_input}")
            try:
                response_data = resp.json()
                st.session_state.past_results = response_data
                st.success("Past results retrieved successfully!")
            except json.JSONDecodeError:
                st.error(f"Error: Invalid response format. Status code: {resp.status_code}")
        else:
            st.error("Please enter both JD ID and Resume ID")
    
    # Display past results if available
    if 'past_results' in st.session_state:
        st.markdown('<div class="section-header">Score / Result</div>', unsafe_allow_html=True)
        
        # Create scoring grid
        score_col1, score_col2 = st.columns(2)
        
        with score_col1:
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Hard Scoring</div>
                <div class="score-value">{st.session_state.past_results.get("hard_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Verdict</div>
                <div class="score-value">{st.session_state.past_results.get("verdict", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with score_col2:
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Semantic Scoring</div>
                <div class="score-value">{st.session_state.past_results.get("semantic_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="score-card">
                <div class="score-title">Overall Scoring</div>
                <div class="score-value">{st.session_state.past_results.get("overall_score", "N/A")}</div>
            </div>
            ''', unsafe_allow_html=True)