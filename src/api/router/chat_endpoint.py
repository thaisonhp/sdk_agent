from fastapi import APIRouter, WebSocket
from api.schemas import QueryRequest
from fastapi import HTTPException , UploadFile, File
from domain.runner import run_agent
import os 
from dotenv import load_dotenv
import shutil
import openai
import os 
load_dotenv()
from agents import RunContextWrapper
from src.domain.runner import stream_agent_response


chat_router = APIRouter()

@chat_router.get("/")
async def read_root():
    return {"message": "Hello World"}

@chat_router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    print("📡 WebSocket connected!")

    try:
        while True:
            # Nhận tin nhắn từ client
            user_message = await websocket.receive_text()
            print(f"📝 User: {user_message}")

            # Kiểm tra API Key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                await websocket.send_text("⚠️ Vui lòng nhập API key trước khi sử dụng!")
                continue

            # Gọi Agent để xử lý tin nhắn
            answer = await run_agent(user_message=user_message)
            
            # Gửi phản hồi về client
            await websocket.send_text(answer)
            print(f"🤖 AI: {answer}")

    except Exception as e:
        print(f"❌ Lỗi WebSocket: {e}")
    finally:
        print("🔌 WebSocket disconnected!")
        await websocket.close()
@chat_router.post("/ask/")
async def ask_question(request: QueryRequest):
    """
    API endpoint to ask a question to the AI model.

    Args:
        request (QueryRequest): The request containing article and question.

    Returns:
        dict: A response containing the answer from the AI model.
    """
    try:
        # Gọi hàm chạy agent
        user_message = request.text
        print(f"📝 User: {user_message}")
        # response = await run_agent(user_message=user_message)
        # return {"answer": response}
        return await stream_agent_response(user_message)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @chat_router.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     """
#     API endpoint to upload a file and store it in OpenAI's storage.

#     Args:
#         file (UploadFile): The uploaded file from client.

#     Returns:
#         dict: A response containing file ID and filename.
#     """
#     try:
#         # Lưu file tạm thời
#         temp_file_path = f"temp_{file.filename}"
#         with open(temp_file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Gọi hàm upload file lên OpenAI
#         client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         file_id = create_file(client, temp_file_path)

#         # Xóa file tạm sau khi upload
#         os.remove(temp_file_path)

#         return {"filename": file.filename, "file_id": file_id}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
