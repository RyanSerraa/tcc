import pandas as pd

from src.domain.state import State


class Supervisor:
    def __init__(self, agente):
        self.supervisor_agent = agente
        self.departamentos_set = set(
            pd.read_csv("src/resources/depts.csv", header=None)[0].str.lower()
        )

    def choose_chain(self, state: State, embeddings, connection):
        question = state.question.lower()
        hasFoundDept = any(dep.lower() in question for dep in self.departamentos_set)
        contexto = embeddings.getContext(state.question, "supervisor", connection)
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
