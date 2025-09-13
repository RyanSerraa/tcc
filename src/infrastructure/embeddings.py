from langchain_huggingface import HuggingFaceEmbeddings
from psycopg2.extras import DictCursor, Json


class Embeddings:
    def __init__(self):
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
        )

    def embed_query(self, question: str):
        return self.embeddings_model.embed_query(question)

    def getContext(self, question: str, agente: str, connection) -> str:
        query_emb = self.embed_query(question)
        query_emb_vector = Json(query_emb)
        resultados = []

        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT pergunta, resposta
                FROM rag_documentos
                WHERE agente = %s
                ORDER BY embedding_pergunta <-> %s::vector
                LIMIT 5
                """,
                (agente, query_emb_vector),
            )
            resultados = cursor.fetchall()

        contexto = "\n".join(
            [
                f"{i+1}. Pergunta: {r['pergunta']}\n   Resposta: {r['resposta']}"
                for i, r in enumerate(resultados)
            ]
        )
        return contexto
