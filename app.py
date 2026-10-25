from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "homefix_db")
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return render_template("index.html")

from flask import request, redirect, url_for, flash
from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = None
        cur = None

        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                "SELECT id, name, email, password_hash FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()

            if user and check_password_hash(
                user["password_hash"], password
            ):
                return redirect(url_for("home"))

            return render_template(
                "login.html",
                message="Email ya password galat hai."
            )

        except Exception as e:
            app.logger.exception("Login error")
            return render_template(
                "login.html",
                message="Login mein problem hai. Database connection check karein."
            ), 500

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template("login.html")

@app.route("/api/appliances", methods=["GET"])
def appliances():
    defaults = ["AC", "Refrigerator", "Washing Machine", "Fan", "Microwave", "Water Heater"]
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT appliance FROM troubleshooting_rules ORDER BY appliance")
        rows = [r[0] for r in cur.fetchall()]
        cur.close(); conn.close()
        return jsonify(rows or defaults)
    except Error:
        return jsonify(defaults)

@app.route("/api/troubleshoot", methods=["POST"])
def troubleshoot():
    data = request.get_json(silent=True) or {}
    appliance = (data.get("appliance") or "").strip()
    symptom = (data.get("symptom") or "").strip()
    if not appliance or not symptom:
        return jsonify({"error": "Please select an appliance and enter its problem."}), 400
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, appliance, symptom, possible_cause, solution, safety_warning
            FROM troubleshooting_rules
            WHERE LOWER(appliance) = LOWER(%s)
              AND (LOWER(symptom) LIKE CONCAT('%%', LOWER(%s), '%%')
                   OR LOWER(%s) LIKE CONCAT('%%', LOWER(symptom), '%%'))
            ORDER BY id LIMIT 5
        """, (appliance, symptom, symptom))
        results = cur.fetchall()
        cur.close(); conn.close()
        if not results:
            results = [{
                "id": None, "appliance": appliance, "symptom": symptom,
                "possible_cause": "The exact cause could not be identified from the available rules.",
                "solution": "Check the user manual, make sure the appliance is being used as instructed, and contact an authorized technician if the problem continues.",
                "safety_warning": "Do not open the appliance or touch internal wiring. Unplug it only if it is safe to do so. If you smell burning, see sparks, or notice smoke, keep away and get help."
            }]
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO repair_history (appliance, symptom, result_summary) VALUES (%s, %s, %s)",
                    (appliance, symptom, results[0]["possible_cause"]))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"results": results, "technician_recommended": any(
            "technician" in (r.get("solution") or "").lower() for r in results)})
    except Error as e:
        return jsonify({"error": "Cannot connect to MySQL. Please check database setup and run database.sql. Details: " + str(e)}), 500

@app.route("/api/history", methods=["GET"])
def history():
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, appliance, symptom, result_summary, created_at FROM repair_history ORDER BY id DESC LIMIT 30")
        rows = cur.fetchall()
        cur.close(); conn.close()
        for row in rows:
            if row.get("created_at"):
                row["created_at"] = row["created_at"].strftime("%d %b %Y, %I:%M %p")
        return jsonify(rows)
    except Error as e:
        return jsonify({"error": "Database connection failed. Check MySQL settings. " + str(e)}), 500

@app.route("/api/technician", methods=["POST"])
def technician():
    data = request.get_json(silent=True) or {}
    appliance = (data.get("appliance") or "Home appliance").strip()
    return jsonify({
        "message": "For safety, contact an authorized appliance service centre or qualified technician.",
        "checklist": [
            "Keep the appliance switched off if it seems unsafe.",
            "Do not remove covers or attempt electrical repairs.",
            "Share the appliance model and symptoms with the technician.",
            "Mention any burning smell, unusual noise, leakage, or error code."
        ],
        "appliance": appliance
    })
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "register.html",
                message="Please fill all fields."
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                message="Password kam se kam 8 characters ka hona chahiye."
            )

        conn = None
        cur = None

        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            if cur.fetchone():
                return render_template(
                    "register.html",
                    message="Ye email pehle se registered hai."
                )

            password_hash = generate_password_hash(password)

            cur.execute(
                "INSERT INTO users (name, email, password_hash) "
                "VALUES (%s, %s, %s)",
                (name, email, password_hash)
            )

            conn.commit()
            return redirect(url_for("login"))

        except Exception:
            app.logger.exception("Registration error")
            return render_template(
                "register.html",
                message="Registration mein problem hai. Terminal check karein."
            ), 500

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
