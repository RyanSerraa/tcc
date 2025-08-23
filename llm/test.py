import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2

load_dotenv()
# Cria a URL de conexão
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(os.environ["DATABASE_URL"])

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)
