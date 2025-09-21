# 📄 Automated Resume Relevance Check System

An AI-powered system that evaluates student resumes against job descriptions (JDs), scores relevance, and provides actionable feedback — built for a hackathon to help placement teams shortlist candidates faster.

## ✨ Features

- Upload JDs & Resumes (PDF / DOCX / TXT) via dashboard
- Robust text extraction (pdfplumber, docx2txt)
- Smart parsing into sections: skills, education, projects, experience
- Skill matching
    - __Hard match:__ must-have & nice-to-have with fuzzy matching
    - __Semantic match:__ embeddings + cosine similarity
- Weighted scoring (0–100) with verdicts: High / Medium / Low
- Actionable feedback (missing skills, improvement tips)
- Recruiter dashboard built with Streamlit
- Extendable: add skills via `skills_list.json`

## 🏗️ Architecture

```
Resume / JD Upload
            ↓
     Extractor
            ↓
        Parser
            ↓
    ┌─────────────┐
    │Skill Matching│
    └─────────────┘
        ↓         ↓
Hard/Fuzzy   Embeddings
    Score       → Semantic Score
         \         /
            → Weighted Final Score →
                                Verdict + Feedback →
                                    Streamlit Dashboard
```


## 📂 Project Structure

```
resume-relevance/
    ├── backend/  
    │   ├── app.py                # API endpoints (Flask/FastAPI)  
    │   ├── extractor.py          # PDF/DOCX text extraction  
    │   ├── parser.py             # JD & Resume parsing, skills extraction  
    │   ├── evaluator.py          # Orchestration of evaluation  
    │   ├── scoring.py            # Hard + semantic scoring logic  
    │   ├── embeddings.py         # sentence-transformers + FAISS integration  
    │   ├── llm_feedback.py       # Optional LLM-based suggestions  
    │   └── requirements.txt      # Python dependencies  
    ├── dashboard/  
    │   └── streamlit_app.py      # Recruiter dashboard  
    ├── scripts/  
    │   └── seed_skills.py        # Generate/update skills_list.json  
    ├── skills_list.json          # Canonical skills list  
    └── README.md
```

# ⚙️ Installation

### 1. Clone repository
```bash
git clone https://github.com/your-username/resume-relevance.git
cd resume-relevance
```

## 2. Create a virtual environment
```bash
    python -m venv venv

    # macOS / Linux
    source venv/bin/activate

    # Windows
    venv\Scripts\activate
```

## 3. Install dependencies
```bash
    pip install -r backend/requirements.txt
```

## 4. Download SpaCy model
```bash
    python -m spacy download en_core_web_sm
```

## 🚀 Running the Project

Flask:
```bash
cd backend
python app.py
```

Frontend (Streamlit dashboard):
```bash
cd dashboard
streamlit run streamlit_app.py
```

Open the dashboard: http://localhost:8501

## Usage Flow

1. Upload Job Description (JD) in the sidebar  
2. Provide must-have & nice-to-have skills (optional) or auto-extract from JD  
3. Upload candidate resume  
4. System extracts text, parses skills, computes scores  
5. Returns verdict (High / Medium / Low) with missing skills & tips  
6. Recruiters can view and fetch stored evaluations in the dashboard


## Scoring

- Hard Match: 70% weight
    - Must-have skills weighted higher
    - Nice-to-have skills add bonus points
- Semantic Match: 30% weight
    - Cosine similarity on embeddings
- Final Score: Weighted sum (0–100)
- Verdict thresholds:
    - ≥ 75 → High Fit
    - ≥ 50 → Medium Fit
    - < 50 → Low Fit
- Note: If a must-have skill is missing, the score may be capped.


## Example Output

```json
{
    "resume_id": "r1",
    "score": 82.5,
    "verdict": "High",
    "hard_score": 85.0,
    "semantic_score": 80.0,
    "missing_skills": ["Docker"],
    "resume_skills": ["Python", "AWS", "SQL"]
}
```

## 👥 Team

- Siddeshwar Sharma (https://github.com/Siddeshwar1412)
- Vishwajith Veludandi (https://github.com/Tagorevishwa)
- Charan Yama (https://github.com/charan-the-dev)

## 📜 License

MIT License © 2025 Hackathon Team