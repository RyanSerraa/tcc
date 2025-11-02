from src.domain.state import State
from src.infrastructure.db import DB


class Supervisor:
    def __init__(self, agente):
        self.supervisor_agent = agente

    def choose_chain(self, state: State, embeddings, db: DB):
        question = state.question.lower()
        depts = db.execute_query(
            f"""
            SELECT d.nome
            FROM ddepartamento d
            WHERE '{question}' ILIKE CONCAT('%', d.nome, '%') AND d.nome IS NOT NULL
            """
        )
        hasFoundDept = depts != []
        contexto = embeddings.getContext(state.question, "supervisor", db)
        prompt = (
            f"Contexto relevante:\n{contexto}\n"
            f'Pergunta do usuário: "{state.question}".\n'
            f"temDepartamentoEncontrado: {hasFoundDept}"
        )
        response = self.supervisor_agent.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        resposta_texto = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        return {"isEUA": resposta_texto.lower() == "sim"}
