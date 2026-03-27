import logging
from graph.state import VideoState

logger = logging.getLogger(__name__)

def audio_agent(state: VideoState) -> VideoState:
    logger.info(f"[{state['job_id']}] audio_agent MOCK")
    state["audio_url"] = f"s3://videogen-assets-574772738554/audio/{state['job_id']}.mp3"
    state["status"] = "audio_done"
    return state