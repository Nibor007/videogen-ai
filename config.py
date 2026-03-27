from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    FREEPIK_API_KEY: str = ""
    FISH_API_KEY: str = ""
    FISH_VOICE_ID: str = ""
    VIDEO_SERVICE_URL: str = "https://tu-servicio-video.com/api/assemble"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "videogen-assets-574772738554"
    DATABASE_URL: str
    SQS_QUEUE_URL: str = ""
    SQS_DLQ_URL: str = ""
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_PROJECT: str = "videogen-ai"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()