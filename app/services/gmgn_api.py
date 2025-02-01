import asyncio
import os
import json
from typing import Optional, Dict, Any
from pydantic import BaseModel
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

class GMGNResponse(BaseModel):
    markdown: str
    status: str
    error: Optional[str] = None

async def get_gmgn_info(token_address: str) -> GMGNResponse:
    """
    Fetch token information from GMGN.ai
    
    Args:
        token_address: The token address to look up
        
    Returns:
        GMGNResponse object containing the markdown data and status
    """
    try:
        url = f"https://gmgn.ai/base/token/VIVOWmEQ_{token_address}"
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url)
            
            if not result or not result.markdown:
                return GMGNResponse(
                    markdown="",
                    status="error",
                    error="Failed to fetch data from GMGN.ai"
                )
            
            return GMGNResponse(
                markdown=result.markdown,
                status="success"
            )
            
    except Exception as e:
        return GMGNResponse(
            markdown="",
            status="error",
            error=str(e)
        )
