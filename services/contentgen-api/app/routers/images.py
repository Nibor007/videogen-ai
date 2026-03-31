from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import logging

from app.services.bedrock import generate_image
from app.services.storage import upload_image

logger = logging.getLogger(__name__)
router = APIRouter()

class ImageStyle(str, Enum):
    photorealistic = "photorealistic"
    cinematic      = "cinematic"
    illustration   = "illustration"
    anime          = "anime"

class ImageSize(str, Enum):
    square    = "1024x1024"
    landscape = "1152x768"
    portrait  = "768x1152"

class GenerateImageRequest(BaseModel):
    prompt:          str        = Field(..., min_length=3, max_length=1000)
    negative_prompt: str        = Field(default="blurry, low quality, distorted")
    style:           ImageStyle = ImageStyle.photorealistic
    size:            ImageSize  = ImageSize.square
    num_images:      int        = Field(default=1, ge=1, le=4)
    seed:            Optional[int] = None

class GenerateImageResponse(BaseModel):
    job_id:     str
    status:     str
    images:     list[str]
    model:      str
    prompt:     str
    created_at: str

@router.post("/image", response_model=GenerateImageResponse)
async def create_image(req: GenerateImageRequest):
    import uuid
    from datetime import datetime

    job_id = str(uuid.uuid4())
    logger.info(f"[{job_id}] Generating image — prompt='{req.prompt[:60]}'")

    try:
        images_bytes = await generate_image(req)
        urls = []
        for i, img_bytes in enumerate(images_bytes):
            url = await upload_image(img_bytes, job_id, i)
            urls.append(url)
    except Exception as e:
        logger.error(f"[{job_id}] Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(f"[{job_id}] Done — {len(urls)} image(s)")

    return GenerateImageResponse(
        job_id     = job_id,
        status     = "completed",
        images     = urls,
        model      = "amazon.nova-canvas-v1:0",
        prompt     = req.prompt,
        created_at = datetime.utcnow().isoformat() + "Z",
    )