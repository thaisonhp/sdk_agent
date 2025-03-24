from agents import Agent
from src.application.get_weather import get_the_weather_today
import os 
from src.domain.tracing import TracingHooks
prompt = "Bạn là một trợ lý hữu ích, hãy sử dụng công cụ của bạn để trả lời câu hỏi."

weather_agent = Agent(
    name="Weather Agent",
    instructions= prompt ,
    model=os.getenv("MODEL_AGENT_NAME"),
    tools=[get_the_weather_today] ,
    hooks=TracingHooks("Weather Agent")
)

