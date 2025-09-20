import json

from src.domain.state import State


class Gerente:
    def __init__(self, agente):
        self.gerente_agent = agente

    def choose_chain(self, state: State):
        prompt = f'Pergunta do usuário: "{state.question}".\n' f"Dados: {state.result}"
        response = self.gerente_agent.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        decision = json.loads(content)
        print(f"Gerente decision: {decision}")
        return {"gerente_decision": decision}
