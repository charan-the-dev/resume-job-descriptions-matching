# backend/evaluator.py
from extractor import extract_text_from_upload
from parser import split_by_sections, extract_skills_from_text, extract_education
from embeddings import EmbedStore
from scoring import hard_match_score, semantic_score, final_score, verdict_from_score

embed_store = EmbedStore()


def evaluate_resume(uploaded_resume, jd_text, jd_parsed_skills):
    import json

    with open("../scripts/seed_skills.json") as f:
        SKILL_LIST = json.load(f)

    resume_text = extract_text_from_upload(uploaded_resume)
    sections = split_by_sections(resume_text)
    resume_skills = extract_skills_from_text(resume_text, skill_list=SKILL_LIST)
    hard = hard_match_score(jd_parsed_skills, resume_skills)
    sem = semantic_score(jd_text, resume_text, embed_store)
    score = final_score(hard, sem, weights=(0.5, 0.5))
    verdict = verdict_from_score(score)

    # missing skills = must skills not found
    missing = []
    must = (
        jd_parsed_skills.get("must", jd_parsed_skills)
        if isinstance(jd_parsed_skills, dict)
        else jd_parsed_skills
    )
    from fuzzywuzzy import fuzz

    for m in must:
        found = any(
            fuzz.token_sort_ratio(m.lower(), r.lower()) >= 85 for r in resume_skills
        )
        if not found:
            missing.append(m)
    return {
        "score": score,
        "verdict": verdict,
        "hard_score": hard,
        "semantic_score": sem,
        "missing_skills": missing,
        "resume_skills": resume_skills,
        "sections": sections,
    }
