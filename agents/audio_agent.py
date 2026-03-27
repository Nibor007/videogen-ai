import logging
import httpx
import boto3
from config import settings
from graph.state import VideoState

logger = logging.getLogger(__name__)

def audio_agent(state: VideoState) -> VideoState:
    logger.info(f"[{state['job_id']}] audio_agent iniciado")
    try:
        narracion = " ".join(
            e["narracion"] for e in state["script"]["escenas"]
        )

        # 🔥 FISH AUDIO REQUEST
        response = httpx.post(
            "https://api.fish.audio/v1/tts",
            headers={
                "Authorization": f"Bearer {settings.FISH_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "text": narracion,
                "voice": settings.FISH_VOICE_ID,  # 👈 define esto en tu config
                "format": "mp3"
            },
            timeout=120.0
        )

        response.raise_for_status()

        # 🔥 SUBIR A S3
        s3 = boto3.client("s3", region_name=settings.AWS_REGION)
        key = f"audio/{state['job_id']}.mp3"

        s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=response.content,
            ContentType="audio/mpeg"
        )

        state["audio_url"] = f"s3://{settings.S3_BUCKET}/{key}"
        state["status"] = "audio_done"

        logger.info(f"[{state['job_id']}] audio guardado en S3")

    except Exception as e:
        logger.error(f"[{state['job_id']}] audio_agent error: {e}")
        state["errors"].append(f"audio: {str(e)}")
        state["retry_count"] += 1

    return state