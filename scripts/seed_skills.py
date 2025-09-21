# scripts/seed_skills.py
DEFAULT_SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "react",
    "node.js",
    "django",
    "flask",
]

# Save to JSON file for backend to load and use for matching
import json

with open("skills_list.json", "w") as f:
    json.dump(DEFAULT_SKILLS, f, indent=2)
print("Saved skills_list.json")
