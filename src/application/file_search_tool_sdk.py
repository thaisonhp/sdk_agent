from agents import FileSearchTool  , function_tool
import openai
import os 

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ API Key không được tìm thấy! Hãy kiểm tra lại biến môi trường.")

client = openai.OpenAI(api_key=api_key)

# Tạo vector store mới
vector_store = client.vector_stores.create(name="MyFileStore") 

# Lấy ID của vector store
vector_store_id = vector_store.id
print(f"Vector Store ID: {vector_store_id}")


# Tải tệp lên OpenAI
file_response = client.files.create(
    file=open("data_test/VanBanGoc_52.2014.QH13.pdf", "rb"),
    purpose="assistants"
)

# Lấy ID của tệp đã tải lên
file_id = file_response.id
print(f"File ID: {file_id}")

# Thêm tệp vào vector store
client.vector_stores.files.create(
    vector_store_id=vector_store_id,
    file_id=file_id
)
print("Tệp đã được thêm vào Vector Store.")


def search_marriage_law(query: str):
    """
    Search for marriage law regulations in the vector store.
    
    Args:
        vector_store_id (str): The ID of the vector store containing legal documents.
        query (str): The question or keyword to search for.
    
    Returns:
        list: A list of search results.
    """
    # Initialize the FileSearchTool
    file_search = FileSearchTool(
        vector_store_ids=[vector_store_id],  
        max_num_results=3  # Limit the number of returned results
    )

    # Perform the search query
    results = file_search
    # Display the search results
    print("Search Results:", results)
    return results


# Chạy công cụ tìm kiếm tệp 

query = "Divorce regulations under marriage law"
search_marriage_law(query)
