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
from services.crewat import crew,gngm_crew
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

from typing import List
from services.deepseek import get_deepseek_completion

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


@app.get("/token-price")
def get_token_price(token_address: str):
    price_data = fetch_token_price(token_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])
    return price_data


@app.post("/analyze-token-price")
async def analyze_token_price(token_pair_address: str):
    # Fetch the token price
    price_data = fetch_token_price(token_pair_address)
    if "error" in price_data:
        raise HTTPException(status_code=400, detail=price_data["error"])

    # print({"price_data": price_data})

    # Kickoff the analysis with the token price data
    analysis_result = crew.kickoff(inputs={"data": price_data})
    return analysis_result


@app.get("/gmgn-info")
async def get_gmgn_token_info(token_address: str):
    base_url = "https://gmgn.ai/base/token/VIVOWmEQ_"
    url = operator.concat(base_url, token_address)
    response = await crawl_gmgn(url)
    if response is None:
        raise HTTPException(status_code=400, detail=response.error if response else "Error fetching GMGN data")
    analysis_result=gngm_crew.kickoff(inputs={"data":response})
    return analysis_result


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


@app.get("/twitter-search", response_model=TwitterSearchResponse)
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

    return response


class Metric(BaseModel):
    name: str
    value: str
    change: str


class SocialMetrics(BaseModel):
    social_mentions: Metric
    sentiment_score: Metric
    influencer_reach: Metric
    community_growth: Metric


class RiskMetrics(BaseModel):
    overall_risk_score: Metric
    smart_contract_safety: Metric
    liquidity_lock_status: Metric


class Alert(BaseModel):
    title: str
    description: str
    priority: str
    timestamp: str


class AlertsNotification(BaseModel):
    active_alerts: int
    triggered_today: int
    success_rate: str
    response_time: str
    alerts: List[Alert]


class AIAndRiskResponse(BaseModel):
    social_metrics: SocialMetrics
    ai_signal_strength: Metric
    risk_metrics: RiskMetrics
    alerts_notification: AlertsNotification


@app.get("/metrics", response_model=AIAndRiskResponse)
async def get_metrics():
    response_data = AIAndRiskResponse(
        social_metrics=SocialMetrics(
            social_mentions=Metric(
                name="Social Mentions (24h)", value="12,458", change="↑ 425%"
            ),
            sentiment_score=Metric(
                name="Sentiment Score", value="7.8/10", change="↑ 2.1"
            ),
            influencer_reach=Metric(
                name="Influencer Reach", value="2.5M", change="↓ 12%"
            ),
            community_growth=Metric(
                name="Community Growth", value="+15.4K", change="↑ 28%"
            ),
        ),
        ai_signal_strength=Metric(
            name="Overall Signal Strength",
            value="Strong Buy",
            change="Confidence: 85%",
        ),
        risk_metrics=RiskMetrics(
            overall_risk_score=Metric(
                name="Overall Risk Score",
                value="Medium Risk",
                change="Risk Level: 6.5/10",
            ),
            smart_contract_safety=Metric(
                name="Smart Contract Safety",
                value="85%",
                change="Audited & Verified",
            ),
            liquidity_lock_status=Metric(
                name="Liquidity Lock Status",
                value="Locked",
                change="180 Days Remaining",
            ),
        ),
        alerts_notification=AlertsNotification(
            active_alerts=24,
            triggered_today=8,
            success_rate="92%",
            response_time="1.2s",
            alerts=[
                Alert(
                    title="Critical: Social Mention Spike",
                    description="PEPE +450% mentions in last 4h",
                    priority="High Priority",
                    timestamp="Triggered 5 minutes ago",
                ),
                Alert(
                    title="Warning: Liquidity Change",
                    description="DOGE -18% liquidity in 24h",
                    priority="Medium Priority",
                    timestamp="Triggered 15 minutes ago",
                ),
                Alert(
                    title="Info: Volume Increase",
                    description="SHIB 2.5x average volume",
                    priority="Low Priority",
                    timestamp="Triggered 30 minutes ago",
                ),
            ],
        ),
    )

    return response_data


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
