import json
import logging
import boto3
import time
from graph.graph import graph
from graph.state import VideoState
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s"
)
logger = logging.getLogger(__name__)

sqs = boto3.client("sqs", region_name=settings.AWS_REGION)

def process_message(message: dict) -> bool:
    try:
        body = json.loads(message["Body"])
        job_id = body["job_id"]
        prompt = body["prompt"]

        logger.info(f"[{job_id}] Procesando job desde SQS")

        initial_state = VideoState(
            prompt=prompt,
            job_id=job_id,
            script=None,
            audio_url=None,
            images=None,
            video_url=None,
            errors=[],
            retry_count=0,
            status="pending"
        )

        graph.invoke(
            initial_state,
            config={
                "configurable": {"thread_id": job_id},
                "recursion_limit": 50
            }
        )

        logger.info(f"[{job_id}] Job completado")
        return True

    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        return False

def run():
    logger.info("Worker SQS iniciado — esperando mensajes...")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=settings.SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,        # Long polling
                VisibilityTimeout=300      # 5 minutos para procesar
            )

            messages = response.get("Messages", [])

            if not messages:
                continue

            for message in messages:
                success = process_message(message)

                if success:
                    # Eliminar mensaje de la cola
                    sqs.delete_message(
                        QueueUrl=settings.SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    logger.info("Mensaje eliminado de SQS")
                else:
                    # No eliminar — SQS lo reintentará
                    # Después de 3 intentos va a la DLQ
                    logger.warning("Mensaje no procesado — SQS reintentará")

        except Exception as e:
            logger.error(f"Error en el worker loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()