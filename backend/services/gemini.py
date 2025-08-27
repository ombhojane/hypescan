import os
import google.generativeai as genai
from typing import Dict, Any

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

async def analyze_gmgn_data(gmgn_data: str) -> Dict[str, Any]:

    prompt = f"""

    You are an expert in analyzing GMGN.ai data.
    You are given a GMGN.ai data of a token.
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


            Raw Data:
            {gmgn_data}

            Format the response as a clean JSON object without any markdown formatting or additional headers. Include all available metrics and insights from the provided data. """
    
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    
    return {
        "analysis": response.text,
        "status": "success"
    }