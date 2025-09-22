from myapi import db

class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=True)     
    source = db.Column(db.String, nullable=True)
    severity = db.Column(db.String, nullable=True)
