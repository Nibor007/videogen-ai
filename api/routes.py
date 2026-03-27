from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from graph.graph import graph
from graph.state import VideoState

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str

@router.post("/generate", status_code=202)
async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    initial_state = VideoState(
        prompt=req.prompt,
        job_id=job_id,
        script=None,
        audio_url=None,
        images=None,
        video_url=None,
        errors=[],
        retry_count=0,
        status="pending"
    )
    background_tasks.add_task(
        graph.invoke,
        initial_state,
        config={"configurable": {"thread_id": job_id}}
    )
    return {"job_id": job_id, "status": "processing"}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    try:
        config = {"configurable": {"thread_id": job_id}}
        state = graph.get_state(config)

        if not state or not state.values:
            raise HTTPException(status_code=404, detail="Job no encontrado")

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