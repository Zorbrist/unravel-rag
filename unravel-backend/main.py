import zipfile
import os
from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()

MAX_FILE_SIZE = 50 * 1024 * 1024        # 50 MB limit
MAX_UNCOMPRESSED_SIZE = 250 * 1024 * 1024 # 250 MB limit
UPLOADED_FILE_DIRECTORY = os.path.abspath("./uploaded_files")

@app.post("/upload_file")
async def upload_file(file: UploadFile):
    
    # validate the file is a zip file
    if not file.filename.lower().endswith('.zip'):
        raise HTTPException(status_code=400, detail="Ivalid file format, please upload a zip file ")
    
    #validate size of the compressed zip file 
    file.file.seek(0, os.SEEK_END)
    compressed_file = file.file.tell()
    file.file.seek(0)
    
    if compressed_file > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Zip file too big")
    
    if not zipfile.is_zipfile(file.file):
        raise HTTPException(status_code=400, detail="Invalid ZIP archive structure")
    file.file.seek(0)
    
    try:
        with zipfile.ZipFile(file.file,'r') as zip_ref:
           total_compressed_size = 0
           
           for member in zip_ref.infolist():
               
               target_path = os.path.abspath(os.path.join(UPLOADED_FILE_DIRECTORY, member.filename))
               
               # Zip Slip check
               if not target_path.startswith(UPLOADED_FILE_DIRECTORY + os.sep) and target_path != UPLOADED_FILE_DIRECTORY:
                   raise HTTPException(status_code=400, detail="Malicios file path detected")
               
               # overload check / Zip Bomb
               total_compressed_size += member.file_size
               if total_compressed_size > MAX_UNCOMPRESSED_SIZE:
                   raise HTTPException(status_code=400, detail="Uncompressed size is too large")
                 
           os.makedirs(UPLOADED_FILE_DIRECTORY, exist_ok=True)
           zip_ref.extractall(UPLOADED_FILE_DIRECTORY)
               
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Corrupted archive")

    return {"status": "Success", "extracted_to": UPLOADED_FILE_DIRECTORY}
