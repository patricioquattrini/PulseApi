from sqlalchemy import delete
from models.alerts import Alerts
from models.users import Users
from models.base import AsyncSessionLocal

async def delete_saved_items(items):
    if not items:
        return
    ids = [item["id"] for item in items]
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Alerts).where(Alerts.id.in_(ids)))
            await session.execute(delete(Users).where(Users.id.in_(ids)))
        await session.commit()
