import io
import json
import os
import subprocess

import requests
from bson import ObjectId
from docx import Document
from loguru import logger
from pydantic import EmailStr

from core.config import settings
from messages.utils.html import generate_table_html, replace_table_with_html
from models.chunks import chunk_manager
from models.documents import doc_manager
from src.chunkr import chunkr_client
from src.minio import minio_client

from .celery import app

# ----------------------------------------------------------------


@app.task()
def convert_and_create_task(file: bytes,
                            doc_id: str,
                            dir_path: str,
                            email: str,
                            file_name: str,
                            projectId: str):
    doc = Document(io.BytesIO(file))
    random_docx_name = os.path.join(dir_path, f"tmp/{doc_id}.docx")
    # save original file
    try:
        doc.save(random_docx_name)

        # Convert DOCX to PDF using LibreOffice in headless mode
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', "--outdir",
                       f"{dir_path}/data", random_docx_name], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during LibreOffice conversion: {e}")

    finally:
        # Ensure that the temporary DOCX file is removed after conversion
        if os.path.exists(random_docx_name):
            os.remove(random_docx_name)
    minio_client.upload_file(file_name=f"{doc_id}.pdf",
                             file_path=f"{dir_path}/data/{doc_id}.pdf",
                             target_dir="origin")
    os.remove(f"{dir_path}/data/{doc_id}.pdf")

    # process table and chunking
    for table in doc.tables:
        html = generate_table_html(table)
        replace_table_with_html(doc, table, html)
    random_docx_name = os.path.join(dir_path, f"tmp/{doc_id}.docx")
    try:
        doc.save(random_docx_name)

        # Convert DOCX to PDF using LibreOffice in headless mode
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', "--outdir",
                       f"{dir_path}/data", random_docx_name], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during LibreOffice conversion: {e}")

    finally:
        # Ensure that the temporary DOCX file is removed after conversion
        if os.path.exists(random_docx_name):
            os.remove(random_docx_name)
    minio_client.upload_file(file_name=f"{doc_id}.pdf",
                             file_path=f"{dir_path}/data/{doc_id}.pdf",
                             target_dir="doc")

    task_id = chunkr_client.create_task(
        file=open(f"{dir_path}/data/{doc_id}.pdf", "rb"))
    doc_manager.insert_doc(id=doc_id,
                           email=email,
                           file_name=file_name,
                           task_id=task_id,
                           projectId=projectId)
    os.remove(f"{dir_path}/data/{doc_id}.pdf")


@app.task()
def upload_file_to_vs(content: str,
                      doc_id: str,
                      page_number: int,
                      vector_store_id: str):
    # 1. upload to vector store
    url_create_file = "https://api.openai.com/v1/files"
    headers = {
        'Authorization': f'Bearer {settings.OPENAI_KEY}',
    }
    file_id = str(ObjectId())
    files = {
        'file': (f"{file_id}.txt", content)
    }
    data_crreate_file = {
        'purpose': 'assistants'
    }
    response_create_file = (requests.post(url=url_create_file,
                                          headers=headers,
                                          data=data_crreate_file,
                                          files=files)).json()
    logger.info(str(response_create_file))
    # 2. create vector file
    url_create_vector = f'https://api.openai.com/v1/vector_stores/{vector_store_id}/files'

    data_create_vector = {
        'file_id': response_create_file["id"],
        'chunking_strategy': {
            'type': 'static',
            'static': {'max_chunk_size_tokens': 4000,
                       'chunk_overlap_tokens': 0}
        }
    }
    response_vector = requests.post(url=url_create_vector,
                                    headers={
                                        'Authorization': f'Bearer {settings.OPENAI_KEY}',
                                        'Content-Type': 'application/json',
                                        'OpenAI-Beta': 'assistants=v2'
                                    },
                                    data=json.dumps(data_create_vector)).json()
    logger.info(str(response_vector))
    # update database
    chunk_manager.insert_chunk(content=content,
                               documentId=doc_id,
                               vector_id=response_create_file["id"],
                               id=file_id,
                               page_number=page_number,
                               vectore_store_id=vector_store_id)


@app.task()
def delete_file_vector_store(file_id):
    # Delete file in openAI vector store
    url = f"https://api.openai.com/v1/files/{file_id}"
    requests.delete(url=url, headers={"Authorization": f"Bearer {settings.OPENAI_KEY}"})
    # Delete file in database
    chunk_manager.delete_chunk(vector_id=file_id)
    