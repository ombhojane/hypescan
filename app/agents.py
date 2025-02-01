from crewai import Agent, LLM
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3, api_key=api_key)
# Data Analyzer Agent
analyzer = Agent(
    role="Data Analyzer",
    goal="Analyze cryptocurrency data and provide insights based on key metrics.",
    backstory="An expert in blockchain and crypto data analysis, providing insights on price trends, liquidity, market activity, and other key metrics.",
    verbose=True,
    llm=llm
)