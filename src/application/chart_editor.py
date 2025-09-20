from src.domain.state import State


class ChartEditor:
    def __init__(self, agent):
        self.chart_editor = agent

    def respond(self, state: State):
        refazer_grafico = state.redator_response.get("redoChart")
        base_prompt = f'Pergunta: "{state.question}".\nDados: "{state.result}".\n'
        if refazer_grafico:
            base_prompt += f"Refazer gráfico: {state.chartEditor_response}\n"
        response = self.chart_editor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": base_prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"chartEditor_response": content}
