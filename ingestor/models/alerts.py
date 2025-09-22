from utils import Utils
from typing import Any, Dict
from .base import Base, AsyncSessionLocal
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone

class Alerts(Base):
    __tablename__ = "alerts"  
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    user_id = Column(String, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow) 
    created_alert = Column(DateTime, nullable=True)
    detected_alert = Column(DateTime, nullable=True)
    source = Column(String, nullable=True)
    severity = Column(String, nullable=True)
Index("idx_user_id", Alerts.user_id)

def parse_iso_to_naive(dt_str: str) -> datetime:
    if dt_str is None:
        return None
    # Convierte ISO string con Z a datetime aware en UTC
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    # Convierte a naive (quita tzinfo)
    return dt.astimezone(timezone.utc).replace(tzinfo=None)

async def save_history(item: Dict[str, Any]) -> None:
    stmt = insert(Alerts).values(
        id=item["id"],
        email=item["email"].lower(),
        user_id=Utils.email_to_id(item["email"].lower()),
        created_at=datetime.utcnow(),                 
        created_alert=parse_iso_to_naive(item.get("created_at")),
        detected_alert=parse_iso_to_naive(item.get("detected_at")),
        source=(item.get("source_info") or {}).get("source"),
        severity=(item.get("source_info") or {}).get("severity")
    ).on_conflict_do_nothing(index_elements=[Alerts.id])

    async with AsyncSessionLocal() as db:
        async with db.begin():
            await db.execute(stmt)
