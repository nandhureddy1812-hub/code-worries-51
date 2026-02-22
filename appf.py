from ocr import extract_text
from utils import clean_text
from validator import validate_document
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
import pytesseract
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)


app.secret_key = "docverify_secret"
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store uploaded files per user
user_uploads = {}

users = {}

DOCUMENTS = {
    "ugcet": {
        "BTech": ["10th Marksheet", "12th Marksheet", "CET Score Card", "Photo ID (Aadhaar)"],
        "Agriculture": ["10th Marksheet", "12th Marksheet", "CET Score Card", "Photo ID (Aadhaar)"]
    },
    "pgcet": {
        "MBA": ["UG Degree Certificate", "PGCET Score Card", "Photo ID (Aadhaar)"],
        "MCA": ["UG Degree Certificate", "PGCET Score Card", "Photo ID (Aadhaar)"]
    }
}

EXAM_INFO = {
    "ugcet": {
        "title": "UGCET",
        "full_name": "Under Graduate Common Entrance Test",
        "description": "For admission to undergraduate programs",
        "documents": ["10th Marksheet", "12th Marksheet", "CET Score Card", "Photo ID (Aadhaar)"]
    },
    "pgcet": {
        "title": "PGCET",
        "full_name": "Post Graduate Common Entrance Test",
        "description": "For admission to postgraduate programs",
        "documents": ["UG Degree Certificate", "PGCET Score Card", "Photo ID (Aadhaar)"]
    }
}

# Home page → choose login or signup
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    mobile = request.form["mobile"]

    if email in users:
        return render_template("auth.html", error="Email already exists")

    users[email] = {
        "password": password,
        "mobile": mobile
    }

    # Automatically log in the user after signup
    session["user"] = email
    return redirect(url_for("category"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    if email in users and users[email]["password"] == password:
        session["user"] = email
        return redirect(url_for("category"))
    else:
        return "Invalid Credentials"

@app.route("/category")
def category():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("category.html", exam_info=EXAM_INFO)

@app.route("/documents", methods=["POST"])
def documents():
    exam = request.form["exam"]
    course = request.form["course"]
    required_docs = DOCUMENTS.get(exam, {}).get(course, [])
    return render_template("documents.html",
                           exam=exam,
                           course=course,
                           documents=required_docs)

@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    file = request.files["file"]
    doc_name = request.form.get("doc_name")

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    user_email = session["user"]

    filename = f"{user_email}_{doc_name}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # --- Show realistic processing ---
    time.sleep(1.5)

    # --- OCR ---
    print("Saved file path:", file_path)
    text = extract_text(file_path)
    text = clean_text(text)

    print("===== OCR TEXT =====")
    print(text)
    print("====================")

    # --- VALIDATION ---
    fields, confidence = validate_document(text, doc_name)

    status = "Valid" if confidence >= 60 else "Invalid"

    return jsonify({
        "success": True,
        "document": doc_name,
        "confidence": confidence,
        "status": status,
        "fields": fields
    })
@app.route("/get_uploads", methods=["GET"])
def get_uploads():
    if "user" not in session:
        return jsonify({}), 401
    
    user_email = session["user"]
    return jsonify(user_uploads.get(user_email, {}))

@app.route("/submit", methods=["POST"])
def submit():
    uploaded = request.form.getlist("uploaded_docs")
    total_docs = int(request.form["total_docs"])
    uploaded_count = len(uploaded)
    percentage = int((uploaded_count / total_docs) * 100) if total_docs > 0 else 0

    return render_template("result.html",
                           uploaded_count=uploaded_count,
                           total_docs=total_docs,
                           percentage=percentage)

@app.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("home"))
    
    uploaded_count = int(request.args.get("uploaded", 0))
    total_docs = int(request.args.get("total", 0))
    percentage = int((uploaded_count / total_docs) * 100) if total_docs > 0 else 0
    
    return render_template("result.html",
                           uploaded_count=uploaded_count,
                           total_docs=total_docs,
                           percentage=percentage)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
