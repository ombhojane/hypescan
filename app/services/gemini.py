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
    Please format this Raw data and get useful information from it.

    {gmgn_data}
    
    Please give response in JSON format without any additional headers like "```json" or "```.
    """
    
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    
    return {
        "analysis": response.text,
        "status": "success"
    }