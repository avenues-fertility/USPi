from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import List
import os
import shutil
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)


def check_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API Key',
        )
    return api_key


@app.get('/')
async def show_status():
    return 'server is running!'


@app.post('/upload')
async def upload_files(files: List[UploadFile] = File(...),
                       api_key: str = Depends(check_api_key)):
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    return {'saved': saved_files}
