from myapi import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    score = db.Column(db.Integer, unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "score": self.score}
    
    def get_score(self):
        return {"score": self.score}
    
