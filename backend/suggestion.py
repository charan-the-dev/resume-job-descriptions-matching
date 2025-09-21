# backend/llm_feedback.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_feedback(jd_text, resume_text, missing_skills, top_n=5):
    prompt = f"""
You are a helpful recruiter assistant.

Job requirements:
{jd_text[:2000]}

Candidate resume (concise):
{resume_text[:2000]}

Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}

Provide:
1) Short summary (1-2 lines) comparing candidate to the JD.
2) Top 5 actionable suggestions the candidate can follow to improve fit (certs, projects, keywords to add, upskilling).
3) One-sentence suggestion to the recruiter for shortlisting.

Format as JSON: {{ "summary": "...", "suggestions": ["..."], "recruiter_note":"..." }}
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # use a suitable available model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350,
        temperature=0.2,
    )
    text = resp["choices"][0]["message"]["content"]
    return text  # in practice parse JSON returned
