import re
import spacy
import json
from collections import defaultdict
from fuzzywuzzy import fuzz

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Load canonical skills (seeded from skills_list.json)
try:
    with open("skills_list.json") as f:
        CANONICAL_SKILLS = json.load(f)
except FileNotFoundError:
    CANONICAL_SKILLS = []  # fallback if file missing

# Stopwords / fluff words that appear in JDs but are not real skills
STOPWORDS = [
    "experience",
    "knowledge",
    "ability",
    "familiarity",
    "understanding",
    "proficiency",
    "background",
    "excellent",
    "strong",
    "good",
    "communication",
    "skills",
    "team",
    "player",
]

# Section headers
SECTION_HEADERS = [
    "experience",
    "education",
    "skills",
    "projects",
    "certifications",
    "summary",
    "technical skills",
]


def clean_jd_text(text: str) -> str:
    """
    Remove fluff/stopwords from JD text.
    """
    for sw in STOPWORDS:
        text = re.sub(rf"\b{sw}\b", "", text, flags=re.I)
    return text


def split_by_sections(text: str):
    """
    Split resume text into sections based on common headers.
    """
    lines = text.splitlines()
    sections = defaultdict(list)
    current = "header"
    for ln in lines:
        stripped = ln.strip()
        if any(
            re.search(r"^" + h + r"[:\s]*$", stripped, flags=re.I)
            for h in SECTION_HEADERS
        ):
            current = stripped.lower()
            continue
        sections[current].append(ln)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_skills_from_text(text: str, skill_list=None, threshold=80):
    """
    Extract skills from text.
    1. Prefer canonical skill list (with fuzzy match).
    2. If no canonical matches found, fall back to heuristic noun extraction.
    """
    if skill_list is None:
        skill_list = CANONICAL_SKILLS

    found_skills = set()
    text_lower = text.lower()

    # --- Step 1: Fuzzy match against canonical list ---
    for sk in skill_list:
        if fuzz.partial_ratio(sk.lower(), text_lower) >= threshold:
            found_skills.add(sk)

    # --- Step 2: Heuristic fallback if not enough skills found ---
    if len(found_skills) < 3:  # if too few skills detected
        doc = nlp(text)
        for token in doc:
            if (
                token.pos_ in ("NOUN", "PROPN")
                and token.text.isalnum()
                and len(token.text) > 2
            ):
                if token.text.lower() not in STOPWORDS:
                    found_skills.add(token.text)

    return list(found_skills)


def extract_education(text: str):
    """
    Extract degrees/education from text.
    """
    ed = []
    patterns = [
        r"(Bachelor(?:'s)?|B\.Sc|B\.Tech|BE|BS)\b.*\d{4}",
        r"(Master(?:'s)?|M\.Sc|MCA|M\.Tech|MS)\b.*\d{4}",
        r"(\bph\.?d\b|\bdoctorate\b)",
    ]
    for p in patterns:
        found = re.findall(p, text, flags=re.I)
        if found:
            ed.extend(found)
    return ed
