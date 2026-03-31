import logging
from graph.state import VideoState

logger = logging.getLogger(__name__)

def video_agent(state: VideoState) -> VideoState:
    logger.info(f"[{state['job_id']}] video_agent MOCK")
    state["video_url"] = f"https://videogen-assets-574772738554.s3.amazonaws.com/videos/{state['job_id']}.mp4"
    state["status"] = "done"
    return state