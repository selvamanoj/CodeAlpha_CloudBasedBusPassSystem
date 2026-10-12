import os, re, sqlite3
from datetime import date, datetime
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "bus_pass.db"))
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")

def get_db():
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL,
            email TEXT NOT NULL, phone TEXT NOT NULL, route_name TEXT NOT NULL,
            pass_type TEXT NOT NULL, start_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending', created_at TEXT NOT NULL)""")

def valid_email(value):
    return bool(re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", value))

@app.route("/")
def index():
    init_db()
    with get_db() as db:
        applications = db.execute("SELECT * FROM applications ORDER BY id DESC LIMIT 100").fetchall()
        total = db.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        pending = db.execute("SELECT COUNT(*) FROM applications WHERE status=?", ("Pending",)).fetchone()[0]
        approved = db.execute("SELECT COUNT(*) FROM applications WHERE status=?", ("Approved",)).fetchone()[0]
        rejected = db.execute("SELECT COUNT(*) FROM applications WHERE status=?", ("Rejected",)).fetchone()[0]
    return render_template("index.html", applications=applications, total=total, pending=pending,
                           approved=approved, rejected=rejected, today=date.today().isoformat())

@app.route("/apply", methods=["POST"])
def apply():
    init_db()
    fields = {key: request.form.get(key, "").strip() for key in
              ("full_name", "email", "phone", "route_name", "pass_type", "start_date")}
    if not all(fields.values()):
        flash("Please complete all fields.", "error")
        return redirect(url_for("index"))
    if not valid_email(fields["email"].lower()):
        flash("Enter a valid email address.", "error")
        return redirect(url_for("index"))
    if not re.fullmatch(r"[0-9+\\-\\s()]{7,20}", fields["phone"]):
        flash("Enter a valid phone number.", "error")
        return redirect(url_for("index"))
    if fields["pass_type"] not in {"Daily", "Weekly", "Monthly", "Student"}:
        flash("Choose a valid pass type.", "error")
        return redirect(url_for("index"))
    try:
        date.fromisoformat(fields["start_date"])
    except ValueError:
        flash("Choose a valid start date.", "error")
        return redirect(url_for("index"))
    with get_db() as db:
        db.execute("""INSERT INTO applications
            (full_name,email,phone,route_name,pass_type,start_date,status,created_at)
            VALUES (?,?,?,?,?,?,?,?)""",
            (fields["full_name"], fields["email"].lower(), fields["phone"], fields["route_name"],
             fields["pass_type"], fields["start_date"], "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    flash("Application submitted successfully. Status: Pending.", "success")
    return redirect(url_for("index"))

@app.route("/applications/<int:application_id>/status", methods=["POST"])
def update_status(application_id):
    status = request.form.get("status", "")
    if status not in {"Pending", "Approved", "Rejected"}:
        flash("Invalid application status.", "error")
        return redirect(url_for("index"))
    with get_db() as db:
        cursor = db.execute("UPDATE applications SET status=? WHERE id=?", (status, application_id))
    flash(f"Application #{application_id} updated to {status}." if cursor.rowcount else "Application not found.",
          "success" if cursor.rowcount else "error")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    try:
        init_db()
        with get_db() as db:
            db.execute("SELECT 1").fetchone()
        return {"status": "healthy", "database": "connected"}, 200
    except sqlite3.Error:
        return {"status": "unhealthy", "database": "error"}, 500

init_db()
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=True)
