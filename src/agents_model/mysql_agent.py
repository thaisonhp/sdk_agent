from agents import Agent
from src.application.database_processor import get_all_infor_building, get_building_by_id, get_building_by_name, get_building_by_ward
import os 
from src.domain.tracing import TracingHooks
# from agents_model.basic_qa_agent import basic_QA_agent
prompt = """Bạn là trợ lý hỗ trợ khách hàng nếu họ hỏi về vấn đề nhà chung cư thì bạn hãy hỏi họ muốn biết thông tin gì để tìm kiếm thông tin cho họ .
  hãy báo cho họ là đang có các phương thức tìm theo phường và tên chung cư . Hãy sử dụng tool phù hợp với thông tin họ cấp
 nếu không phải chung cư thì bạn không trả lời và chuyển cho agent khác phù hợp
 """

mysql_agnet = Agent(
    name="MySQL Agent",
    instructions=prompt,
    model= os.getenv("MODEL_AGENT_NAME"),
    tools=[get_all_infor_building, get_building_by_id, get_building_by_name, get_building_by_ward],
    # handoffs=[basic_QA_agent]
    hooks=TracingHooks("MySQL Agent")
)