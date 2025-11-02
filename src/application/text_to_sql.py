from src.domain.state import State
from src.infrastructure.db import DB


class TextToSQL:
    def __init__(self, agente):
        self.text_to_sql = agente

    def to_sql_query(self, state: State, embeddings, db: DB):
        contexto = embeddings.getContext(state.question, "text_to_sql", db)
        final_prompt = (
            f"Pergunta do usuario:\n{state.question}\n\nContexto relevante:\n{contexto}"
        )
        response = self.text_to_sql.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": final_prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = "".join(choice.message.content for choice in response.choices)
        cleanedQuery = self.clean_text(content)
        return {"query": cleanedQuery}

    @staticmethod
    def clean_text(text: str) -> str:
        keywords = [
            "insert",
            "delete",
            "update",
            "drop",
            "create",
            "alter",
            "truncate",
            "merge",
            "call",
            "exec",
        ]
        for keyword in keywords:
            if keyword.lower() in text.lower():
                return ""
        return text
