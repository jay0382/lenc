import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o conteúdo do .env

DB_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DB_URL)

def buscar_url(alias):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT url_real FROM links WHERE alias = %s", (alias,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
