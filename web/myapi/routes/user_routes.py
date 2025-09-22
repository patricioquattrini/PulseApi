from flask import jsonify, request
from myapi.models.user import User
from myapi.models.alert import Alert
from myapi import db
import hashlib

def register_user_routes(app):
    @app.route("/api/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])

    @app.route("/api/user", methods=["POST"])
    def get_score():
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Email requerido"}), 400
        email = data["email"]
        user_id = hashlib.sha256(email.encode("utf-8")).hexdigest()
        print(user_id)
        user = User.query.get_or_404(user_id)
        return jsonify(user.get_score())

    @app.route("/api/alerts", methods=["POST"])
    def get_alerts():
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Email requerido"}), 400
        email = data["email"]
        user_id = hashlib.sha256(email.encode("utf-8")).hexdigest()
        print(user_id)
        alerts = Alert.query.filter_by(user_id=user_id).all()
        if not alerts:
            return jsonify({"error": "No se encontraron alertas para este usuario"}), 404
        return jsonify([{"id": a.id,"email": a.email,"source": a.source,"severity": a.severity} for a in alerts])

