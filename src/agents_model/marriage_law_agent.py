from agents import Agent, FileSearchTool , Runner
import os
from src.domain.tracing import TracingHooks

# Tạo công cụ tìm kiếm tài liệu
vector_store_id = "vs_67e0b64bbf148191be2be638a906e484"  
file_search_tool = FileSearchTool(
    vector_store_ids=[vector_store_id],
    max_num_results=3,  
    include_search_results=True  
)

# Tạo Agent chuyên tìm kiếm luật hôn nhân
marriage_law_agent = Agent(
    name="Marriage Law Agent",
    instructions="""Bạn là một trợ lý pháp lý chuyên tìm kiếm luật hôn nhân và gia đình tại Việt Nam.
    Nếu khách hàng đặt câu hỏi về luật hôn nhân, hãy sử dụng công cụ của bạn để tìm kiếm câu trả lời trong tài liệu pháp lý.
    Lưu ý : hãy nói tên tài liệu bạn dùng để trả lời cho người dùng biết để họ có thể tham khảo thêm thông tin.
    """,
    model=os.getenv("MODEL_AGENT_NAME"),
    tools=[file_search_tool],  
    hooks=TracingHooks("Marriage Law Agent")  
)
