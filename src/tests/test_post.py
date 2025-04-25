from httpx import AsyncClient
from typing import Dict


async def create_post(body: str, async_clinet: AsyncClient) -> dict:
    response = await async_clinet.post("/post", json={"body": body})
    return response.json()
