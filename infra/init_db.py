import psycopg
from langgraph.checkpoint.postgres import PostgresSaver

DATABASE_URL = "postgresql://videogenadmin:VideoGen2024!@videogen-db.cupmsgwqevte.us-east-1.rds.amazonaws.com:5432/videogen"

with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()
    print("Tablas de LangGraph creadas correctamente.")