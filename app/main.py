from fastapi import FastAPI
from app.routes import scan
from app.logger import get_logger

app = FastAPI(title="ClamAV Daemon Scan API")
logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("ClamAV Daemon Scan API started and ready")

app.include_router(scan.router, prefix="/api")
