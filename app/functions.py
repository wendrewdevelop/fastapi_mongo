from app.config import app


async def save_address(address: dict):
    app.db.insert_one(address)