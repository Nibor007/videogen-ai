from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from graph.state import VideoState
from graph.conditions import after_script, after_video
from agents.script_agent import script_agent
from agents.audio_agent import audio_agent
from agents.images_agent import images_agent
from agents.video_agent import video_agent
from config import settings
import psycopg

def build_graph():
    builder = StateGraph(VideoState)

    builder.add_node("run_script", script_agent)
    builder.add_node("run_audio", audio_agent)
    builder.add_node("run_images", images_agent)
    builder.add_node("run_video", video_agent)

    builder.set_entry_point("run_script")

    builder.add_conditional_edges("run_script", after_script, {
        "next": "run_audio",
        "retry": "run_script"
    })

    builder.add_edge("run_audio", "run_images")
    builder.add_edge("run_images", "run_video")

    builder.add_conditional_edges("run_video", after_video, {
        "end": END,
        "retry": "run_video"
    })

    conn = psycopg.connect(settings.DATABASE_URL, autocommit=True)
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()

    #return builder.compile(checkpointer=checkpointer)
    return builder.compile(
        checkpointer=checkpointer,
        debug=False
    )

graph = build_graph()