import requests
from io import BytesIO
from typing import Union
from openai import OpenAI

def create_file(client: OpenAI, file_path: str) -> str:
    """
    Uploads a file to OpenAI's storage, either from a local path or a URL.

    Args:
        client (OpenAI): An instance of the OpenAI client.
        file_path (str): The file path (local) or URL (remote) of the file to be uploaded.

    Returns:
        str: The unique ID of the uploaded file.

    Raises:
        requests.RequestException: If the file download from URL fails.
        openai.error.OpenAIError: If the file upload to OpenAI fails.
    """
    if file_path.startswith(("http://", "https://")):
        # Download the file content from the URL
        response = requests.get(file_path)
        response.raise_for_status()  # Raise an error for failed requests

        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)

        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )

    print(result.id)
    return result.id
