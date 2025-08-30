from src.domain.state import State


class ChartEditor:
    def __init__(self, agent):
        self.chart_editor = agent

    def respond(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\".\nDados: \"{state['result']}\".\n"
        response = self.chart_editor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"answer": answer}
