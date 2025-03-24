from agents import Agent
import os 
from src.domain.tracing import TracingHooks
from src.application.calculate_pit import calculate_pit_in_vn
import os 
pit_agent = Agent(
    name="Pit Agent",
    instructions="""Bạn là một trợ lý chuyên tư vấn về thuế thu nhập cá nhân .
     Nếu khách hàng có nhu cầu về tính thu nhập cá nhân hãy sử dụng công cụ của bạn để tư vấn cho họ
     Nếu thấy họ chưa đề cập đến income hoặc dependents hãy hỏi cho đến khi họ cung cấp đủ thông tin
    khi cung cấp đủ thông tin hãy sử dụng công cụ để tính toán và trả lời cho họ""",
    model=os.getenv("MODEL_AGENT_NAME"),
    tools=[calculate_pit_in_vn],
    hooks =TracingHooks("Pit Agent")
)