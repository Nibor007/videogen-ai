import boto3, json, base64, os, asyncio, logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.routers.images import GenerateImageRequest

logger = logging.getLogger(__name__)

REGION   = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_IMAGE_MODEL", "amazon.nova-canvas-v1:0")

STYLE_PROMPTS = {
    "photorealistic": "photorealistic, highly detailed, 8k, professional photography",
    "cinematic":      "cinematic, dramatic lighting, film grain, anamorphic lens",
    "illustration":   "digital illustration, vibrant colors, concept art",
    "anime":          "anime style, detailed, clean lines, vibrant colors",
}

SIZE_MAP = {
    "1024x1024": {"width": 1024, "height": 1024},
    "1152x768":  {"width": 1152, "height": 768},
    "768x1152":  {"width": 768,  "height": 1152},
}

def _get_client():
    return boto3.client("bedrock-runtime", region_name=REGION)

def _build_nova_canvas_payload(req) -> dict:
    size   = SIZE_MAP[req.size]
    prompt = f"{req.prompt}, {STYLE_PROMPTS[req.style]}"

    payload = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text":         prompt,
            "negativeText": req.negative_prompt,
        },
        "imageGenerationConfig": {
            "numberOfImages": req.num_images,
            "width":          size["width"],
            "height":         size["height"],
            "cfgScale":       7.5,
            "quality":        "premium",
        },
    }

    if req.seed is not None:
        payload["imageGenerationConfig"]["seed"] = req.seed

    return payload

async def generate_image(req) -> list[bytes]:
    loop    = asyncio.get_event_loop()
    client  = _get_client()
    payload = _build_nova_canvas_payload(req)

    logger.info(f"Calling Bedrock model={MODEL_ID}")

    def _invoke():
        return client.invoke_model(
            modelId     = MODEL_ID,
            contentType = "application/json",
            accept      = "application/json",
            body        = json.dumps(payload),
        )

    response = await loop.run_in_executor(None, _invoke)
    result   = json.loads(response["body"].read())

    if result.get("error"):
        raise Exception(f"Bedrock error: {result['error']}")

    return [base64.b64decode(img["base64"]) for img in result["images"]]