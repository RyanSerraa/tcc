import csv
import os

import psycopg2
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DATABASE_URL = os.getenv("DATABASE_URL_ADMIN")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Lendo CSV
with open("base_conhecimento.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pergunta = row["pergunta"]
        resposta = row["resposta"]
        agente = row["agente"]

        # Gerando embeddings
        emb_pergunta = embeddings_model.embed_query(pergunta)
        emb_resposta = embeddings_model.embed_query(resposta)

        # Inserindo no CockroachDB
        cur.execute(
            """
            INSERT INTO rag_documentos (pergunta, resposta, agente, embedding_pergunta, embedding_resposta)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (pergunta, resposta, agente, emb_pergunta, emb_resposta),
        )

conn.commit()
cur.close()
conn.close()
print("Dados inseridos com sucesso!")
