import boto3, os, asyncio, logging
from datetime import datetime

logger    = logging.getLogger(__name__)
REGION    = os.getenv("AWS_REGION", "us-east-1")
BUCKET    = os.getenv("S3_BUCKET", "videogen-assets-574772738554")
PREFIX    = os.getenv("S3_PREFIX", "contentgen/images")
URL_TTL   = int(os.getenv("PRESIGNED_URL_TTL", "3600"))

def _get_client():
    return boto3.client("s3", region_name=REGION)

async def upload_image(image_bytes: bytes, job_id: str, index: int) -> str:
    loop   = asyncio.get_event_loop()
    client = _get_client()
    key    = f"{PREFIX}/{datetime.utcnow().strftime('%Y/%m/%d')}/{job_id}_{index}.png"

    def _upload():
        client.put_object(
            Bucket      = BUCKET,
            Key         = key,
            Body        = image_bytes,
            ContentType = "image/png",
            Metadata    = {"job_id": job_id},
        )
        return client.generate_presigned_url(
            "get_object",
            Params    = {"Bucket": BUCKET, "Key": key},
            ExpiresIn = URL_TTL,
        )

    url = await loop.run_in_executor(None, _upload)
    logger.info(f"Uploaded: s3://{BUCKET}/{key}")
    return url