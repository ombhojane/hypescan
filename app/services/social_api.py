from pydantic import BaseModel
from typing import List, Optional
import httpx


class RedditSubmission(BaseModel):
    id: str
    title: str
    score: int
    num_comments: int
    permalink: str


class RedditSentimentResponse(BaseModel):
    total_comments: int
    submissions: List[RedditSubmission]


async def get_reddit_sentiment(symbol: str) -> RedditSentimentResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.pushshift.io/reddit/search/submission/?q={symbol}"
        )
        data = response.json()
        submissions = [
            RedditSubmission(**submission)
            for submission in data.get('data', [])
        ]
        return RedditSentimentResponse(
            total_comments=len(submissions), submissions=submissions
        )
