import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API key từ biến môi trường
api_key = os.getenv("OPENAI_API_KEY")

# Kiểm tra xem API key có tồn tại không
if not api_key:
    raise ValueError("⚠️ Lỗi: Chưa thiết lập OPENAI_API_KEY trong file .env!")

# Gán vào biến môi trường
os.environ["OPENAI_API_KEY"] = api_key

print("✅ OPENAI_API_KEY đã được thiết lập thành công!")
