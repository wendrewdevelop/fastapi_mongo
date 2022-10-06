import pytest
from fastapi.testclient import TestClient
from app.main import app
from httpx import AsyncClient


client = TestClient(app)

def test_cep_not_found():
    response = client.get("/search/12420-330")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_async_search_address_by_cep():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/address/12420-330")
	
    assert response.status_code == 200