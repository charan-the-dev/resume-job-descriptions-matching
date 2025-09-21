from flask import Flask, request, jsonify
from extractor import extract_text_from_upload
from parser import extract_skills_from_text
from evaluator import evaluate_resume

app = Flask(__name__)

JDS = {}
RESUMES = {}
EVALS = {}

@app.route("/upload_jd/", methods=["POST"])
def upload_jd():
    file = request.files["file"]
    jd_id = request.form["jd_id"]
    must_skills = request.form.get("must_skills", "")
    nice_skills = request.form.get("nice_skills", "")

    text = extract_text_from_upload(file)
    must = [s.strip() for s in must_skills.split(",")] if must_skills else []
    nice = [s.strip() for s in nice_skills.split(",")] if nice_skills else []
    parsed = {"must": must, "nice": nice}
    if not must:
        parsed["must"] = extract_skills_from_text(text)[:10]

    JDS[jd_id] = {"text": text, "parsed": parsed}
    return jsonify({"jd_id": jd_id, "parsed": parsed})

@app.route("/upload_resume/", methods=["POST"])
def upload_resume():
    file = request.files["file"]
    resume_id = request.form["resume_id"]
    jd_id = request.form["jd_id"]

    jd = JDS.get(jd_id)
    if not jd:
        return jsonify({"error": "JD not found"}), 404

    result = evaluate_resume(file, jd["text"], jd["parsed"])
    RESUMES[resume_id] = {"file": file.filename}
    EVALS[resume_id] = result
    return jsonify({"resume_id": resume_id, "result": result})

@app.route("/get_eval/<resume_id>")
def get_eval(resume_id):
    return jsonify(EVALS.get(resume_id, {"error": "not found"}))

if __name__ == "__main__":
    app.run(port=8000, debug=True)  # 👈 Flask built-in server
