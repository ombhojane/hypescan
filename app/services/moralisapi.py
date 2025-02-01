import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
BASE_CHAIN = 'base'

def fetch_token_price(token_address, chain):
    url = f"https://deep-index.moralis.io/api/v2.2/pairs/{token_address}/stats?chain={chain}"
    
    headers = {
        "Accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": str(err)}

# if __name__ == "__main__":
#     token_address = "0x972798F563AD54d15116672e9b72F84a9054D672"
#     price_data = fetch_token_price(token_address)
#     print(json.dumps(price_data, indent=4)) 
#     # print(price_data)


