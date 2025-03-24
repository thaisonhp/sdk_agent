import requests
from agents import Agent, Runner
import asyncio
from src.agents_model import basic_QA_agent
from src.agents_model import marriage_law_agent
async def run_agent(user_message: str):
    response = await Runner.run(
        starting_agent=basic_QA_agent,
        input=user_message
    )
    return response.final_output

