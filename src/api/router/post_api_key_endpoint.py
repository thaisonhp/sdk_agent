from fastapi import FastAPI, Form
import os 
api_key_router = FastAPI()

@api_key_router.post("/set_api_key/")
async def set_api_key(api_key: str = Form(...)):
    os.environ["OPENAI_API_KEY"] = api_key
    return {"message": "API key đã được lưu!"}
