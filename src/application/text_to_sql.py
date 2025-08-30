import re

from src.domain.state import State


class TextToSQL:
    def __init__(self, agente):
        self.text_to_sql = agente

    def to_sql_query(self, state: State, embeddings, connection):
        cleanedQuestion = state["question"].replace(" em gráfico", "")
        contexto = embeddings.getContext(state["question"], "text_to_sql", connection)
        final_prompt = f"Pergunta do usuario:\n{cleanedQuestion}\n\nContexto relevante:\n{contexto}"
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
        match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r"SELECT .*?;", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return text.strip()
