import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag_service import ingest_document

router = APIRouter()

# Define where to save uploaded files temporarily
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-manual")
async def upload_manual(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF manual, ingest it into the vector DB, and make it searchable.
    """
    if file.filename.split('.')[-1].lower() != 'pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save the file to disk
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger ingestion service
        num_chunks = ingest_document(file_location)
        
        return {
            "message": "Manual uploaded and processed successfully.",
            "filename": file.filename,
            "chunks_created": num_chunks
        }
    
    except Exception as e:
        # Clean up file if processing failed (optional, but good practice)
        # if os.path.exists(file_location):
        #     os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")
