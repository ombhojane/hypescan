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

# Deepseek Analysis Agent
deepseek_analyzer = Agent(
    role="Deepseek Analysis Expert",
    goal="Synthesize and analyze multiple cryptocurrency analysis reports to provide comprehensive insights.",
    backstory="A specialized AI analyst with expertise in combining multiple data sources and analysis reports to generate actionable cryptocurrency insights and predictions.",
    verbose=True,
    llm=llm
)

# Deepseek Analysis Task
deepseek_analysis_task = Task(
    description="Analyze and synthesize the combined outputs from token analysis and GMGN analysis to provide comprehensive insights.",
    agent=deepseek_analyzer,
    goal="Review the token analysis: {token_analysis} and GMGN analysis: {gmgn_analysis}, then provide a comprehensive synthesis with key insights, risks, and potential outcomes.",
    expected_output="deepseek_analysis.md"
)

# Combined Analysis Crew
combined_analysis_crew = Crew(
    agents=[analyzer, gngm_analyzer, deepseek_analyzer],
    tasks=[token_analysis_task, gngm_analysis_task, deepseek_analysis_task],
    llm=llm,
    verbose=True
)