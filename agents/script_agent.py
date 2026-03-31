import json
import logging
from graph.state import VideoState
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)

def script_agent(state: VideoState) -> VideoState:
    logger.info(f"[{state['job_id']}] script_agent iniciado")
    try:
        llm = ChatAnthropic(model="claude-sonnet-4-5")
        response = llm.invoke(f"""
Crea un guión de video de máximo 30 segundos (3 escenas de 10 segundos cada una) para: {state['prompt']}. Narración máximo 2 oraciones por escena.

Responde SOLO con JSON válido, sin texto extra:
{{
    "titulo": "...",
    "escenas": [
        {{
            "numero": 1,
            "narracion": "texto que se narra en voz alta",
            "descripcion_visual": "descripción detallada de la imagen",
            "duracion_seg": 5
        }}
    ]
}}
""")
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        state["script"] = json.loads(raw.strip())
        state["status"] = "script_done"
        logger.info(f"[{state['job_id']}] script generado OK")
    except Exception as e:
        logger.error(f"[{state['job_id']}] script_agent error: {e}")
        state["errors"].append(f"script: {str(e)}")
        state["retry_count"] += 1
    return state