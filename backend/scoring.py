# backend/scoring.py
from fuzzywuzzy import fuzz
import numpy as np


from fuzzywuzzy import fuzz


def hard_match_score(jd_skills, resume_skills):
    if isinstance(jd_skills, dict):
        must = jd_skills.get("must", [])
        nice = jd_skills.get("nice", [])
    else:
        must = jd_skills
        nice = []

    if not must and not nice:
        return 0

    # base weights
    must_weight = 0.8
    nice_weight = 0.2

    # normalize if nice is empty
    if not nice:
        must_weight, nice_weight = 1.0, 0.0
    elif not must:
        must_weight, nice_weight = 0.0, 1.0

    # must score
    must_matches = 0
    for m in must:
        found = False
        for r in resume_skills:
            if fuzz.token_sort_ratio(m.lower(), r.lower()) >= 85:
                found = True
                break  # stop checking once we found a match
        if found:
            must_matches += 1
    must_score = (must_matches / max(1, len(must))) * (must_weight * 100)

    # nice score
    nice_matches = 0
    for n in nice:
        found = False
        for r in resume_skills:
            if fuzz.token_sort_ratio(n.lower(), r.lower()) >= 80:
                found = True
                break
        if found:
            nice_matches += 1
            
    nice_score = (nice_matches / max(1, len(nice))) * (nice_weight * 100)

    return must_score + nice_score


def semantic_score(jd_text, resume_text, embed_store):
    # use embed_store.query to get similarity
    # if the resume is present in meta, find its score; else compute direct cosine
    # Simpler: compute embeddings directly and cosine similarity
    vecs = embed_store.embed([jd_text, resume_text])
    a, b = vecs[0], vecs[1]
    cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    # convert -1..1 to 0..100
    return max(0, (cos + 1) / 2) * 100


def final_score(hard, semantic, weights=(0.7, 0.3)):
    w_hard, w_sem = weights
    return round(hard * w_hard + semantic * w_sem, 2)


def verdict_from_score(score):
    if score >= 75:
        return "High"
    if score >= 50:
        return "Medium"
    return "Low"
