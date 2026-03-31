import logging
from graph.state import VideoState

logger = logging.getLogger(__name__)

def images_agent(state: VideoState) -> VideoState:
    logger.info(f"[{state['job_id']}] images_agent MOCK")
    state["images"] = [
        f"s3://videogen-assets-574772738554/images/{state['job_id']}/escena_{i}.jpg"
        for i in range(1, len(state["script"]["escenas"]) + 1)
    ]
    state["status"] = "images_done"
    return state