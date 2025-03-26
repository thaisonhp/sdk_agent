import requests
from agents import Agent, Runner
import asyncio
from src.agents_model import basic_QA_agent
from src.agents_model import marriage_law_agent
from fastapi.responses import StreamingResponse
async def run_agent(user_message: str):
    response = await Runner.run(
        starting_agent=basic_QA_agent,
        input=user_message
    )
    return response.final_output


async def stream_agent_response(user_message: str):
    """
    Trả về phản hồi của agent theo từng phần.
    """
    response = await run_agent(user_message)

    async def generate():
        for chunk in response.split():  # Giả lập việc gửi từng phần
            yield chunk + " "  # Trả về từng phần nhỏ
            await asyncio.sleep(0.05)  # Giúp hiển thị từ từ

    return StreamingResponse(generate(), media_type="text/plain")