from graph.state import VideoState

def after_script(state: VideoState) -> str:
    if state.get("errors"):
        return "retry"
    return "next"

def after_video(state: VideoState) -> str:
    if state.get("errors"):
        return "retry"
    return "end"