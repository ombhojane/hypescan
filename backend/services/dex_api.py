# from pydantic import BaseModel
# from typing import List
# import httpx
# import asyncio


# class DexPairData(BaseModel):
#     pair_address: str
#     base_token: str
#     quote_token: str
#     price: float
#     liquidity: float
#     volume_24h: float


# class DexResponse(BaseModel):
#     data: List[DexPairData]


# async def get_dex_data(symbol: str) -> DexResponse:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"https://api.dexscreener.com/latest/dex/search?q={symbol}"
#         )
#         response.raise_for_status()
#         data = response.json()
#         return DexResponse(
#             data=[DexPairData(**pair) for pair in data.get('pairs', [])]
#         )

# response = asyncio.run(get_dex_data("GNHW5JetZmW85vAU35KyoDcYoSd3sNWtx5RPMTDJpump"))

# print(response)

import requests

def get_dex_pair_data(chain_id: str, pair_id: str) -> dict:
    """
    Get DEX pair data from DexScreener API
    
    Args:
        chain_id: The blockchain chain ID (e.g., 'ethereum', 'bsc', 'solana')
        pair_id: The pair address/ID
        
    Returns:
        dict: JSON response from the API
    """
    response = requests.get(
        f"https://api.dexscreener.com/latest/dex/pairs/{chain_id}/{pair_id}",
        headers={"Accept": "*/*"},
    )
    response.raise_for_status()
    return response.json()

# print(get_dex_pair_data("solana", "8uAAT95mo699fJ6CMpRw28DKfeVudGkonhEgmNPAEmCE"))