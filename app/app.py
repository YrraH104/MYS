import json
import os

from flask import Flask, jsonify, render_template, request

MSSV = os.environ.get("MSSV", "12345678")
HO_TEN = os.environ.get("HO_TEN", "Ho Ten")
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "students.json")

app = Flask(__name__)


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(students):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


@app.get("/")
def index():
    return render_template("index.html", students=load(), mssv=MSSV, ho_ten=HO_TEN)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "student": MSSV})


@app.get("/api/students")
def list_students():
    students = load()
    lop = request.args.get("lop")
    if lop:
        students = [s for s in students if s["lop"] == lop]
    return jsonify(students)


@app.get("/api/students/<int:sid>")
def get_student(sid):
    for s in load():
        if s["id"] == sid:
            return jsonify(s)
    return jsonify({"error": "not found"}), 404


@app.post("/api/students")
def add_student():
    body = request.get_json(silent=True) or {}
    for field in ("mssv", "ho_ten", "lop", "diem"):
        if field not in body:
            return jsonify({"error": f"thieu truong {field}"}), 400
    diem = body["diem"]
    if isinstance(diem, bool) or not isinstance(diem, (int, float)) or not 0 <= diem <= 10:
        return jsonify({"error": "diem phai tu 0 den 10"}), 400

    students = load()
    new = {
        "id": max((s["id"] for s in students), default=0) + 1,
        "mssv": str(body["mssv"]),
        "ho_ten": body["ho_ten"],
        "lop": body["lop"],
        "diem": diem,
    }
    students.append(new)
    save(students)
    return jsonify(new), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))