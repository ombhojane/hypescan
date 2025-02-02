from crewai import Agent, LLM, Crew, Task
# from tasks import token_analysis_task
import os


api_key = os.getenv("OPENAI_API_KEY")
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3, api_key=api_key)
# Data Analyzer Agent
analyzer = Agent(
    role="Data Analyzer",
    goal="Analyze cryptocurrency data {data} and provide insights based on key metrics.",
    backstory="An expert in blockchain and crypto data analysis, providing insights on price trends, liquidity, market activity, and other key metrics.",
    verbose=True,
    llm=llm
)

# Data Analysis Task
token_analysis_task = Task(
    description="Analyze cryptocurrency token data and provide insights on price trends, liquidity, and market activity.",
    agent=analyzer,
    goal="Provide a detailed analysis of the token {data} and provide insights on price trends, liquidity, and market activity.",
    expected_output="analysis.md"
)

crew = Crew(
    agents=[analyzer,],
    tasks=[token_analysis_task,],
    llm=llm,
    verbose=True
)

gngm_analyzer=Agent(
    role="GMGN Analyzer",
    goal="Analyze the token data {data} and provide insights based on key metrics.",
    backstory="An expert in blockchain and crypto data analysis, providing insights whether the token is a good investment or not.",
    verbose=True,
    llm=llm
)

gngm_analysis_task=Task(
    description="Analyze the token data {data} and provide insights based on key metrics.",
    agent=gngm_analyzer,
    goal="Provide a brief analysis of the token data {data}, and give forcast on whether it is a good investment or not. Do not suggest any recommendations.",
    expected_output="gmgn_analysis.md"
)

gngm_crew=Crew(
    agents=[gngm_analyzer,],
    tasks=[gngm_analysis_task,],
    llm=llm,
    verbose=True
)

twitter_analyzer=Agent(
    role="Twitter Analyzer",
    goal="Analyze the sentiment of the tweets from the twitter data {data} and provide insights based on the sentiment.",
    backstory="An expert in sentiment analysis, providing insights on the mood of the community and how it is affecting the token.",
    verbose=True,
    llm=llm
)

twitter_analysis_task=Task(
    description="Analyze the sentiment of the tweets from the twitter data {data} and provide insights based on the sentiment.",
    agent=twitter_analyzer,
    goal="Provide a brief analysis of the sentiment of the tweets from the twitter data {data}, and give forcast on whether the social sentiment is positive or negative. Provide a score of the sentiment from 0 to 100.",
    expected_output="twitter_analysis.md"
)

twitter_crew=Crew(
    agents=[twitter_analyzer,],
    tasks=[twitter_analysis_task,],
    llm=llm,
    verbose=True
)
