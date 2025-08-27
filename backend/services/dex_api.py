from pydantic import BaseModel
from typing import List, Optional
import httpx


class DexPairData(BaseModel):
    pair_address: str
    base_token: str
    quote_token: str
    price: float
    liquidity: float
    volume_24h: float


class DexResponse(BaseModel):
    data: List[DexPairData]


async def get_dex_data(symbol: str) -> DexResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.dexscreener.com/latest/dex/pairs/{symbol}"
        )
        data = response.json()
        return DexResponse(
            data=[DexPairData(**pair) for pair in data.get('pairs', [])]
        )
