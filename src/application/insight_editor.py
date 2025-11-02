import json

from src.domain.state import State


class InsightEditor:
    def __init__(self, agente):
        self.insight_editor_agent = agente

    def respond(self, state: State):
        prompt = (
            f'Resposta do textEditor: "{state.textEditor_response}"\n'
            f"Resposta do analista: {state.analista_response}\n "
            f"Resposta do chartEditor: {state.chartEditor_response}\n"
            f'Pergunta do usuário: "{state.question}".\n'
            f"Dados: {state.result}"
        )
        response = self.insight_editor_agent.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        response = json.loads(content)
        return {"redator_response": response}
