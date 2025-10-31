import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.clamav_service import ClamAVService
from app.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
clamav_service = ClamAVService()

@router.get("/health")
def health_check():
    logger.info("Performing ClamAV daemon health check")
    healthy = clamav_service.health_check()
    if healthy:
        return {"status": "healthy", "clamd": "running"}
    else:
        raise HTTPException(status_code=503, detail="ClamAV daemon not responding")

@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file for scanning: {file.filename}")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = clamav_service.scan_file(tmp_path)
        os.remove(tmp_path)

        return {
            "file_name": file.filename,
            "status": "CLEAN" if "OK" in result["result"] else "INFECTED",
            "message": result["result"]
        }
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
