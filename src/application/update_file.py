import os
import json
from openai import OpenAI

client = OpenAI()

# Tạo vector store
vector_store = client.vector_stores.create(
    name="Support FAQ",
)

# Thư mục chứa tài liệu
folder_path = "/Users/luongthaison/Documents/Third_years_student/Project/phenika_X/Agent_SDK/data_test/001.LUAT_QLT"
vector_ids = []  # Danh sách lưu vector_id

# Duyệt qua tất cả các file trong thư mục
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path):
        print(f"Uploading {file_name}...")

        # Upload file lên vector store
        response = client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=open(file_path, "rb")
        )

        # Lưu ID của file đã upload
        vector_ids.append({
            "file_name": file_name,
            "vector_id": response.id  # Lấy ID của vector
        })

# Ghi danh sách vector_id vào file JSON
with open("vector_ids.json", "w", encoding="utf-8") as f:
    json.dump(vector_ids, f, indent=4)

 