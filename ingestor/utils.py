import asyncpg
from dotenv import load_dotenv
import os
import hashlib
import asyncio
import unicodedata

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSW = os.getenv("PASSW")
DATABASE_NAME = os.getenv("DATABASE-NAME")
DATABASE_URL = os.getenv("DATABASE-URL")

class Utils:
    @staticmethod
    async def wait_for_db(
        host=HOST, port=PORT, user=USER, password=PASSW, database=DATABASE_NAME
    ):
        for _ in range(5):
            try:
                conn = await asyncpg.connect(
                    host=host, port=port, user=user, password=password, database=database
                )
                await conn.close()
                print("DB lista!")
                return
            except Exception:
                print("Esperando a que la DB esté lista...")
                await asyncio.sleep(2)
        raise Exception("No se pudo conectar a la DB después de varios intentos")

    @staticmethod
    def email_to_id(email: str) -> str:
        def normalize_email(email):
            return unicodedata.normalize("NFC", email)
        email = normalize_email(email)
        return hashlib.sha256(email.lower().encode("utf-8")).hexdigest()