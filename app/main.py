from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.analysis import AgenticAI
from services.coin_api import validate_coin, CoinInfo
from services.social_api import get_reddit_sentiment, RedditSentimentResponse
from services.dex_api import get_dex_data, DexResponse
from forecasting import ForecastData, Prediction
from moralisapi import fetch_token_price

app = FastAPI()


@app.get("/validate-coin", response_model=CoinInfo)
async def validate_coin_endpoint(symbol: str):
    coin_info = await validate_coin(symbol)
    return coin_info


@app.get("/get-social-sentiment", response_model=RedditSentimentResponse)
async def get_sentiment(symbol: str):
    sentiment = await get_reddit_sentiment(symbol)
    return sentiment


@app.get("/forecast", response_model=Prediction)
async def forecast(symbol: str):
    # Fetch data from all sources
    coin_data = await validate_coin(symbol)
    dex_data = await get_dex_data(symbol)
    sentiment = await get_reddit_sentiment(symbol)

    # Combine data into one analysis
    data = {
        "coin_data": coin_data.dict(),
        "dex_data": dex_data.dict(),
        "sentiment": sentiment.dict(),
    }

    # Process with Agentic AI
    ai_model = AgenticAI(data)
    prediction = ai_model.predict()

    return Prediction(
        prediction=prediction['prediction'], confidence=prediction['confidence']
    )

@app.get("/token-price")
def get_token_price(token_address: str, chain: str = BASE_CHAIN):
    price_data = fetch_token_price(token_address, chain)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])
    return price_data

# ... existing code ...