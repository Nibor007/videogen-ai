from typing import TypedDict, List, Optional

class VideoState(TypedDict):
    # Input
    prompt: str
    job_id: str
    
    # Agentes
    script: Optional[dict]
    audio_url: Optional[str]
    images: Optional[List[str]]
    video_url: Optional[str]
    
    # Control
    errors: List[str]
    retry_count: int
    status: str