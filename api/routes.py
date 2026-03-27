from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel
from uuid import uuid4
import boto3
import json
from graph.graph import graph
from graph.state import VideoState
from api.limiter import limiter
from config import settings

router = APIRouter()
sqs = boto3.client("sqs", region_name=settings.AWS_REGION)

class GenerateRequest(BaseModel):
    prompt: str

@router.post("/generate", status_code=202)
@limiter.limit("5/minute")
async def generate_video(request: Request, req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())

    # Guardar estado inicial en RDS via checkpointer
    initial_state = VideoState(
        prompt=req.prompt,
        job_id=job_id,
        script=None,
        audio_url=None,
        images=None,
        video_url=None,
        errors=[],
        retry_count=0,
        status="queued"
    )

    # Encolar en SQS
    sqs.send_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MessageBody=json.dumps({
            "job_id": job_id,
            "prompt": req.prompt
        }),
        MessageAttributes={
            "source": {
                "StringValue": "videogen-api",
                "DataType": "String"
            }
        }
    )

    return {"job_id": job_id, "status": "queued"}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    try:
        config = {"configurable": {"thread_id": job_id}}
        state = graph.get_state(config)

        if not state or not state.values:
            # Job encolado pero aún no procesado
            return {"job_id": job_id, "status": "queued", "video_url": None, "errors": []}

        return {
            "job_id": job_id,
            "status": state.values.get("status", "unknown"),
            "video_url": state.values.get("video_url"),
            "script": state.values.get("script"),
            "errors": state.values.get("errors", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))