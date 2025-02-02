from fastapi import FastAPI, HTTPException
from core.agentic_ai import AgenticAI
from services.coin_api import validate_coin, CoinInfo
from services.social_api import get_reddit_sentiment, RedditSentimentResponse
from services.dex_api import get_dex_data
import operator

# from models.forecasting import Prediction
from services.moralisapi import fetch_token_price
import uvicorn
from services.gmgn_api import get_gmgn_info, GMGNResponse
from services.crewat import crew,gngm_crew,twitter_crew,predict_crew
from services.twitter_api import (
    search_twitter,
    SearchType,
    TwitterSearchResponse,
)
from dotenv import load_dotenv
from services.gemini import analyze_gmgn_data
from pydantic import BaseModel
from services.gmgncrawler import crawl_gmgn
import os
import json

from typing import List
from services.deepseek import get_deepseek_completion

app = FastAPI()
load_dotenv()


# @app.get("/validate-coin", response_model=CoinInfo)
# async def validate_coin_endpoint(symbol: str):
#     coin_info = await validate_coin(symbol)
#     return coin_info
    # sentiment = await get_reddit_sentiment(symbol)
    # return sentiment


@app.get("/token-price")
def get_token_price(token_address: str):
    price_data = fetch_token_price(token_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])
    return price_data


@app.post("/analyze-token-price")
async def analyze_token_price(token_pair_address: str):
    # Fetch the token price
    price_data =get_token_price(token_pair_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])
    price_analysis=crew.kickoff(inputs={"data":price_data})
    return price_analysis


@app.get("/gmgn-info")
async def get_gmgn_token_info(token_address: str):
    base_url = "https://gmgn.ai/base/token/VIVOWmEQ_"
    url = operator.concat(base_url, token_address)
    response = await crawl_gmgn(url)
    if response is None:
        raise HTTPException(status_code=400, detail="Error fetching GMGN data")    
    # Get GMGN analysis
    gmgn_analysis = gngm_crew.kickoff(inputs={"data": response})
    return gmgn_analysis


@app.get("/twitter-search")
async def search_tweets_endpoint(
    query: str, search_type: SearchType = SearchType.TOP, max_tweets: int = 10
):
    # Get Twitter credentials from environment variables
    twitter_username = os.getenv("TWITTER_USERNAME")
    twitter_password = os.getenv("TWITTER_PASSWORD")

    if not twitter_username or not twitter_password:
        raise HTTPException(
            status_code=500, detail="Twitter credentials not configured"
        )

    response = await search_twitter(
        query=query,
        search_type=search_type,
        max_tweets=max_tweets,
        username=twitter_username,
        password=twitter_password,
    )

    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.error)
    response_dict=response.dict()
    # Extract only the tweet texts
    tweets_text_only = {"tweets": [tweet["text"] for tweet in response_dict["tweets"]]}
    # Convert to JSON format
    tweets_json = json.dumps(tweets_text_only, indent=4)
    analysis_result=twitter_crew.kickoff(inputs={"data":tweets_json})
    return analysis_result


# --- Pydantic Models ---
class LiquidityPool(BaseModel):
    platform: str
    pair: str
    liquidity: float
    change: float


class WhaleTransaction(BaseModel):
    address: str
    amount: float
    asset: str
    time_ago: str


class DexAnalyticsResponse(BaseModel):
    total_dex_volume: float
    dex_volume_change: float
    total_liquidity: float
    liquidity_change: float
    unique_traders: int
    traders_change: float
    liquidity_pool: List[LiquidityPool]
    whale_transactions: List[WhaleTransaction]


class FeatureEngineering(BaseModel):
    name: str
    weight: int
    color: str
    value: int


class BlockchainRecognition(BaseModel):
    name: str
    timeFrame: str
    riskColor: str
    riskLevel: str
    riskPercentage: int


class AlertThreshold(BaseModel):
    name: str
    status: str
    color: str
    bgColor: str


class AISignalsResponse(BaseModel):
    strength: str
    confidence: int
    pattern: str
    patternPhase: str
    prediction: str
    forecast: str
    featureEngineering: List[FeatureEngineering]
    blockchainRecognition: List[BlockchainRecognition]
    alertThresholds: List[AlertThreshold]


class RiskAssessmentResponse(BaseModel):
    sectionId: str
    overallRiskScore: str
    riskLevel: str
    smartContractSafetyPercentage: int
    smartContractStatus: str
    liquidityLockStatus: str
    liquidityLockRemainingDays: int
    ownershipStatus: str
    ownershipStatusDescription: str
    mintFunctionStatus: str
    mintFunctionDescription: str
    transferRestrictions: str
    transferRestrictionsDescription: str
    liquidityRisk: str
    liquidityRiskPercentage: int
    concentrationRisk: str
    concentrationRiskPercentage: int
    smartContractRisk: str
    smartContractRiskPercentage: int


class HistoricalResponse(BaseModel):
    roi: int
    pumpPatterns: int
    averagePumpReturn: int
    recoveryTime: int
    activeAlerts: int
    highPriority: int
    triggeredToday: int
    triggeredChange: int
    successRate: int
    responseTime: float


# --- FastAPI Endpoints ---


@app.get("/dex-analytics", response_model=DexAnalyticsResponse)
async def get_dex_analytics(coinAddress: str, pairAddress: str):
    # Logic to fetch data based on coinAddress and pairAddress
    return {
        "total_dex_volume": 1234567890,
        "dex_volume_change": 15.2,
        "total_liquidity": 234567890,
        "liquidity_change": -3.5,
        "unique_traders": 890123,
        "traders_change": 5.4,
        "liquidity_pool": [
            {
                "platform": "Uniswap",
                "pair": "ETH/USDT",
                "liquidity": 50,
                "change": 12.5,
            },
            {
                "platform": "SushiSwap",
                "pair": "BTC/USDT",
                "liquidity": 30,
                "change": -5.2,
            },
        ],
        "whale_transactions": [
            {
                "address": "0x12345...",
                "amount": 500,
                "asset": "ETH",
                "time_ago": "5 minutes ago",
            },
            {
                "address": "0x67890...",
                "amount": -250,
                "asset": "BTC",
                "time_ago": "1 hour ago",
            },
        ],
    }


@app.get("/ai-signals", response_model=AISignalsResponse)
async def get_ai_signals(coinAddress: str, pairAddress: str):
    # Logic to fetch AI signals data based on coinAddress and pairAddress
    return {
        "strength": "Strong Buy",
        "confidence": 85,
        "pattern": "Accumulation",
        "patternPhase": "Phase 2/4",
        "prediction": "+42% Expected",
        "forecast": "24h Forecast",
        "featureEngineering": [
            {
                "name": "Social Volume Velocity",
                "weight": 30,
                "color": "green",
                "value": 85,
            },
            {
                "name": "Influencer Impact",
                "weight": 20,
                "color": "blue",
                "value": 65,
            },
            {
                "name": "Historical Pump Pattern",
                "weight": 25,
                "color": "purple",
                "value": 75,
            },
        ],
        "blockchainRecognition": [
            {
                "name": "Wash Trading Detection",
                "timeFrame": "Last 24 Hours",
                "riskColor": "green",
                "riskLevel": "Low Risk",
                "riskPercentage": 5,
            },
            {
                "name": "Smart Money Movement",
                "timeFrame": "Accumulation Phase",
                "riskColor": "green",
                "riskLevel": "Strong Signal",
                "riskPercentage": 95,
            },
        ],
        "alertThresholds": [
            {
                "name": "Social Mention Spike (+400% in 4h)",
                "status": "Triggered",
                "color": "green",
                "bgColor": "green",
            },
            {
                "name": "Liquidity Change (±15% in 24h)",
                "status": "Warning",
                "color": "yellow",
                "bgColor": "yellow",
            },
            {
                "name": "Transaction Volume (2x 7-day avg)",
                "status": "Normal",
                "color": "gray",
                "bgColor": "gray",
            },
        ],
    }


@app.get("/risk-assessment", response_model=RiskAssessmentResponse)
async def get_risk_assessment(coinAddress: str, pairAddress: str):
    # Logic to fetch risk assessment data based on coinAddress and pairAddress
    return {
        "sectionId": "5a8714c4-1dbf-42ca-8baf-61526238d342",
        "overallRiskScore": "Medium Risk",
        "riskLevel": "6.5/10",
        "smartContractSafetyPercentage": 85,
        "smartContractStatus": "Audited & Verified",
        "liquidityLockStatus": "Locked",
        "liquidityLockRemainingDays": 180,
        "ownershipStatus": "Renounced",
        "ownershipStatusDescription": "Contract ownership has been renounced, reducing rugpull risk",
        "mintFunctionStatus": "Present",
        "mintFunctionDescription": "Contract contains mint function - potential supply inflation risk",
        "transferRestrictions": "Limited",
        "transferRestrictionsDescription": "Max transaction limit: 1% of total supply",
        "liquidityRisk": "Medium",
        "liquidityRiskPercentage": 45,
        "concentrationRisk": "High",
        "concentrationRiskPercentage": 75,
        "smartContractRisk": "Low",
        "smartContractRiskPercentage": 15,
    }


@app.get("/historical", response_model=HistoricalResponse)
async def get_historical_data(coinAddress: str, pairAddress: str):
    # Logic to fetch historical data based on coinAddress and pairAddress
    return {
        "roi": 1245,
        "pumpPatterns": 4,
        "averagePumpReturn": 85,
        "recoveryTime": 48,
        "activeAlerts": 24,
        "highPriority": 12,
        "triggeredToday": 8,
        "triggeredChange": 3,
        "successRate": 92,
        "responseTime": 1.2,
    }


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = 1.0
    max_tokens: int = 1024


@app.post("/chat")
async def chat_completion(request: ChatRequest):
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = await get_deepseek_completion(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/aggregate-analysis")
async def aggregate_analysis(token_pair_address: str, token_address: str, query: str, search_type: SearchType = SearchType.TOP, max_tweets: int = 10):
    # Call analyze_token_price
    price_data = await analyze_token_price(token_pair_address)
    
    # Call get_gmgn_token_info
    gmgn_data = await get_gmgn_token_info(token_address)
    
    # Call search_tweets_endpoint
    tweets_data = await search_tweets_endpoint(query=query, search_type=search_type, max_tweets=max_tweets)
    
    # Combine all outputs into a single JSON response
    combined_output = {
        "price_analysis": price_data.raw,
        "gmgn_info": gmgn_data.raw,
        "tweets_analysis": tweets_data.raw
    }
    predict_output=predict_crew.kickoff(inputs={"data":combined_output})
    return predict_output


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
