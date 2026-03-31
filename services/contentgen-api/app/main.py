from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging, os

from app.routers import images

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ContentGen API starting...")
    yield
    logger.info("ContentGen API shutting down")

app = FastAPI(
    title="ContentGen AI",
    version="0.1.0",
    description="Generación de contenido multimodal con Amazon Bedrock",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router, prefix="/generate", tags=["generation"])

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "contentgen-api",
        "version": "0.1.0",
        "region": os.getenv("AWS_REGION", "us-east-1"),
    }