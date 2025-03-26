import json

def load_vector_store_from_file(file_path: str) -> list:
    """
    Đọc danh sách vector_id từ file JSON và trả về danh sách các ID.

    Args:
        file_path (str): Đường dẫn đến file JSON chứa vector_id.

    Returns:
        list: Danh sách các vector_id.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Trích xuất danh sách ID
        vector_ids = [item["vector_id"] for item in data]
        return vector_ids

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file: {e}")
        return []

