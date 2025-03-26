from agents import Agent, FileSearchTool , Runner
import os
from src.domain.tracing import TracingHooks
from infra.get_vectorstore_id import load_vector_store_from_file
# Tạo công cụ tìm kiếm tài liệu
file_path = "/Users/luongthaison/Documents/Third_years_student/Project/phenika_X/Agent_SDK/vector_ids.json"

vector_store_list = load_vector_store_from_file(file_path)
print(f"Vector Store ID: {vector_store_list[0]}")

file_search_tool = FileSearchTool(
    vector_store_ids= ["vs_67e2452b9d54819198469adf17633c43"],
    max_num_results=3,  
    include_search_results=True 
)

# Tạo Agent chuyên tìm kiếm luật hôn nhân
file_search_agent = Agent(
    name="File search Agent",
    instructions= """ Bạn là một trợ lý chuyên tìm kiếm tài liệu thuế . Khi người dùng có bất kì một câu hỏi liên quan đến văn bản thuê 
    bạn hãy sử dụng công cụ của bạn để tìm kiếm câu trả lời trong tài liệu thuế . Nếu câu hỏi không rõ ràng hãy yêu cầu người dùng cung cấp thêm thông tin""" ,
    model=os.getenv("MODEL_AGENT_NAME"),
    tools=[file_search_tool],  
    hooks=TracingHooks("Marriage Law Agent")  
)
