from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.dialects.postgresql import insert
from .base import Base, AsyncSessionLocal
from utils import Utils
import datetime

class Users(Base):
    __tablename__ = "users" 
    id = Column(String, primary_key=True)
    alert_id = Column(String)
    email = Column(String)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 

async def save_scoring(item):
    score = calculate_score(item)
    hashed_id = Utils.email_to_id(item["email"])

    stmt = insert(Users).values(
        id=hashed_id,
        alert_id=item["id"],
        email=item["email"].lower(),
        score=score
    ).on_conflict_do_update(
        index_elements=[Users.id],  
        set_={
            "score": func.least(Users.score + score, 10)
        }
    )
    async with AsyncSessionLocal() as db:
        async with db.begin():
            await db.execute(stmt)

def calculate_score(alert):
    if alert.get("source_info", {}).get("source") == "malware":
        return 10
    if alert.get("source_info", {}).get("source") == "data breach":
        return 1 if alert.get("source_info", {}).get("severity") == "low" else 3
    return 0
