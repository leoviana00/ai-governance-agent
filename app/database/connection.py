# app/database/connection.py

import psycopg2
import os

# ==========================================
# Configuração de conexão
# ==========================================

DB_HOST = os.getenv("DB_HOST", "172.18.0.3")
DB_NAME = os.getenv("DB_NAME", "aiops")
DB_USER = os.getenv("DB_USER", "aiops")
DB_PASSWORD = os.getenv("DB_PASSWORD", "aiops")
DB_PORT = os.getenv("DB_PORT", "5432")

# ==========================================
# Conexão com banco
# ==========================================

def get_connection():
    """
    Cria conexão com PostgreSQL
    """

    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )