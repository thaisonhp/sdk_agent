from agents import Agent    
import os 
from src.agents_model.mysql_agent import mysql_agnet 
from src.agents_model.weather_agent import weather_agent
from src.agents_model.pit_agent import pit_agent
from src.domain.tracing import TracingHooks
prompt = """Bạn là một trợ lý áo của một công ty về nhà chung cư chuyên chăm sóc khách hàng .
 Hãy tư vấn cho họ thân thiện nhất và nếu có yêu cầu khác mà bạn không sử lý được hay chuyển sang agent khác phù hơp 
 Đặc biệt nếu khách hàng muốn tính thuế thu nhập cá nhân hãy pit_agent"""
basic_QA_agent = Agent(
    name="Basic QA Agent",
    instructions=prompt,
    model=os.getenv("MODEL_AGENT_NAME"),
    handoffs=[mysql_agnet,weather_agent,pit_agent],
    hooks=TracingHooks("Basic QA Agent")

)