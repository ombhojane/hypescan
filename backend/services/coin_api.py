from pydantic import BaseModel
import httpx


class CoinInfo(BaseModel):
    symbol: str
    name: str
    is_valid: bool


async def validate_coin(symbol: str) -> CoinInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.coingecko.com/api/v3/coins/{symbol}"
        )
        data = response.json()
        return CoinInfo(
            symbol=symbol,
            name=data['name'],
            is_valid=True if response.status_code == 200 else False,
        )
