import asyncio
import os
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def crawl_gmgn(token_address):
    browser_config = BrowserConfig(headless=True, verbose=True)
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler(browser_config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://gmgn.ai/base/token/VIVOWmEQ_{token_address}",
            config=crawl_config
        )
        
        if result.success:
            # Configure Gemini
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

            generation_config = {
                "temperature": 0.7, # Lower temperature for more focused output
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[])
            
            prompt = """
            Analyze this token data and provide detailed insights in the following areas:

            1. Top Holders Analysis:
               - Top 10 holder percentages
               - Dev wallet status and transactions
               - Sniper activity and counts
               - Blue chip holder percentage

            2. Security Analysis:
               - Contract verification status
               - Honeypot check results
               - Buy/Sell taxes
               - Risk assessment score
               - Renounced status

            Format the response as a clean JSON object without any markdown formatting or additional headers. Include all available metrics and insights from the provided data.

            Raw Data:
            {data}
"""

            response = chat_session.send_message(prompt.format(data=str(result.markdown)))
            with open("analyzed_token_data_1.json", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Analyzed Token Data saved to analyzed_token_data.json")
            print(response.text)

        else:
            print("Crawl failed")

# asyncio.run(crawl_gmgn("0x93d4e4aafe1eb975244175acd06a6))