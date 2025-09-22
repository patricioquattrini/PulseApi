import asyncio
from tenacity import retry, stop_after_attempt, wait_fixed
import aiohttp
from aiohttp import ClientResponseError
from models.base import Base, engine
from models.alerts import save_history
from models.users import save_scoring
from utils import Utils
from dotenv import load_dotenv
import os
from delete_old_data import delete_saved_items

load_dotenv()

API_BASE = os.getenv("API-BASE")
API_PARAMS = os.getenv("API-PARAMS")
headers = {"x-api-key":os.getenv("API-KEY")}

@retry(wait=wait_fixed(30), stop=stop_after_attempt(5))
async def get_response(session: aiohttp.ClientSession, url: str):
    print(f"Req: {url}")
    try:
        async with session.get(url, headers=headers) as res:
            res.raise_for_status() 
            return await res.json()
    except ClientResponseError as e:
        if e.status == 429:
            sleep = int(e.headers.get("Retry-After", 30))
            print(f"429 Too Many Requests, durmiendo {sleep}s")
            await asyncio.sleep(sleep)
            raise  # tenacity reintentará
        else:
            print(f"HTTP Error {e.status} en {url}")
            raise
    except asyncio.TimeoutError:
        print(f"Timeout al conectar {url}")
        raise
    except Exception as e:
        print(f"Error inesperado {e} en {url}")
        raise

async def get_all_pages(total_pages: int, batch_size: int):
    async with aiohttp.ClientSession() as session:
        all_saved_items = []
        try:
            for i in range(1, total_pages + 1, batch_size):
                batch = list(range(i, min(i + batch_size, total_pages + 1)))

                tasks = [get_response(session, f"{API_BASE}{API_PARAMS}{p}") for p in batch]
                alerts_pages = await asyncio.gather(*tasks, return_exceptions=True)

                items = []
                for page_num, result in zip(batch, alerts_pages):
                    if isinstance(result, Exception):
                        print(f"[ERROR] Página {page_num} falló: {result!r}")
                        raise result 
                    elif isinstance(result, dict) and result.get("alerts"):
                        items.extend(result["alerts"])
                        print(f"[OK] Página Nro {page_num}")

                if items:
                    await asyncio.gather(*(save_scoring(item) for item in items))
                    await asyncio.gather(*(save_history(item) for item in items))
                    all_saved_items.extend(items)

        except Exception as e:
            print("Error! detectado. Se eliminará la data guardada en esta ejecución.")
            await delete_saved_items(all_saved_items)
            raise 


async def init_db():
    await Utils.wait_for_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_db()
    async with aiohttp.ClientSession() as session:
        res = await get_response(session, API_BASE)
        total_pages = res.get("total_pages", 1)
        batch = min(100, round(total_pages*0.1))
        await get_all_pages(total_pages, batch_size=batch)

if __name__ == "__main__":
    asyncio.run(main())
    print("Cerrando Ingestor")
