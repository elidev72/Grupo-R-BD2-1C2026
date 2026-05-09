import os
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from icecream import ic

load_dotenv()

DB_NAME = os.getenv("MONGO_DB_NAME")
DB_HOST = os.getenv("MONGO_HOST")
DB_PORT = int(os.getenv("MONGO_PORT"))

def conectar_db():
    try:
        connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
        ic(f"✅ Conectado a la base de datos: {DB_NAME}")
    except Exception as e:
        ic(f"❌ Error al conectar: {e}")

def desconectar_db():
    disconnect()
    ic("Conexión cerrada.")
