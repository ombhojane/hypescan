from fastapi import FastAPI, HTTPException
from core.agentic_ai import AgenticAI
from services.coin_api import validate_coin, CoinInfo
from services.social_api import get_reddit_sentiment, RedditSentimentResponse
from services.dex_api import get_dex_data
# from models.forecasting import Prediction
from services.moralisapi import fetch_token_price
import uvicorn
from services.gmgn_api import get_gmgn_info, GMGNResponse
from services.crewat import crew
from dotenv import load_dotenv
from services.gemini import analyze_gmgn_data
from pydantic import BaseModel

app = FastAPI()
load_dotenv()

@app.get("/validate-coin", response_model=CoinInfo)
async def validate_coin_endpoint(symbol: str):
    coin_info = await validate_coin(symbol)
    return coin_info


@app.get("/get-social-sentiment", response_model=RedditSentimentResponse)
async def get_sentiment(symbol: str):
    sentiment = await get_reddit_sentiment(symbol)
    return sentiment


# @app.get("/forecast", response_model=Prediction)
# async def forecast(symbol: str):
#     # Fetch data from all sources
#     coin_data = await validate_coin(symbol)
#     dex_data = await get_dex_data(symbol)
#     sentiment = await get_reddit_sentiment(symbol)

#     # Combine data into one analysis
#     data = {
#         "coin_data": coin_data.dict(),
#         "dex_data": dex_data.dict(),
#         "sentiment": sentiment.dict(),
#     }

#     # Process with Agentic AI
#     ai_model = AgenticAI(data)
#     prediction = ai_model.predict()

#     return Prediction(
#         prediction=prediction['prediction'], confidence=prediction['confidence']
#     )

@app.get("/token-price")
def get_token_price(token_address: str):
    price_data = fetch_token_price(token_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])
    return price_data


@app.post("/analyze-token-price")
async def analyze_token_price(token_address: str):
    # Fetch the token price
    price_data = fetch_token_price(token_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])

    print(
        {"price_data":price_data}
    )
    
    # Kickoff the analysis with the token price data
    analysis_result = crew.kickoff(inputs={"data":price_data})
    return analysis_result



@app.get("/gmgn-info", response_model=GMGNResponse)
async def get_gmgn_token_info(token_address: str):
    """
    Get token information from GMGN.ai
    """
    response = await get_gmgn_info(token_address)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.error)
    return response

class AIAnalysisResponse(BaseModel):
    analysis: str
    status: str

@app.get("/analyze-token", response_model=AIAnalysisResponse)
async def analyze_token(token_address: str):
    """
    Get token information from GMGN.ai and analyze it using AI
    """
    # First get GMGN data
    gmgn_response = await get_gmgn_info(token_address)
    if gmgn_response.status == "error":
        raise HTTPException(status_code=400, detail=gmgn_response.error)
    
    # Analyze the data using Gemini
    analysis = await analyze_gmgn_data(gmgn_response.markdown)
    
    return analysis

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
