from fastapi import APIRouter, UploadFile, File

from app.services.data_service import data_service

router = APIRouter()


@router.post("/load-dataframe")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    data_service.load_new_dataframe(content)
    return {"filename": file.filename}
