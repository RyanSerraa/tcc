import json

from src.domain.state import State


class Manager:
    def __init__(self, agente):
        self.manager = agente

    def choose_chain(self, state: State):
        prompt = f'Pergunta do usuário: "{state.question}".\n' f"Dados: {state.result}"
        response = self.manager.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        decision = json.loads(content)
        return {"manager_decision": decision}
