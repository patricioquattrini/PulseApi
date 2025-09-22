from myapi import create_app, db
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask import render_template


app = create_app()

def wait_for_db(retries=10, delay=5):
    for i in range(retries):
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
            print("DB lista")
            return
        except OperationalError:
            print(f"DB no lista, reintentando ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("No se pudo conectar a la DB")

wait_for_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user-alerts")
def user_alerts():
    return render_template("user-alerts.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
