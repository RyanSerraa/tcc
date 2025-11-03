from sentence_transformers import SentenceTransformer
from psycopg2.extras import Json

from src.infrastructure.db import DB


class Embeddings:
    def __init__(self):
        self.embeddings_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
        )

    def embed_query(self, question: str):
        return self.embeddings_model.encode(question)

    def getContext(self, question: str, agente: str, db: DB) -> str:
        query_emb = self.embed_query(question)
        query_emb_list = query_emb.tolist()
        query_emb_vector = Json(query_emb_list)
        resultados = []

        resultados = db.execute_query(
            """
            SELECT pergunta, resposta
            FROM rag_documentos
            WHERE agente = %s
            ORDER BY embedding_pergunta <-> %s::vector
            LIMIT 5
            """,
            (agente, query_emb_vector),
        )

        contexto = "\n".join(
            [
                f"{i+1}. Pergunta: {pergunta}\n   Resposta: {resposta}"
                for i, (pergunta, resposta) in enumerate(resultados)
            ]
        )
        return contexto
