from fastapi import FastAPI
from api.router import chat_router , api_key_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AGENT SDK DEMO")

app.include_router(chat_router)
# app.include_router(api_key_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, OPTIONS...)
    allow_headers=["*"],  # Cho phép tất cả header
)
def start():
    """Hàm khởi chạy FastAPI."""

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="debug")

if __name__ == "__main__":
    start()