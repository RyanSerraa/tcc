from src.domain.state import State


class InsightWriter:
    def __init__(self, agent):
        self.insight_writer = agent

    def respond(self, state: State):
        prompt = f'Pergunta: "{state.question}".\nDados: "{state.result}".\n'
        response = self.insight_writer.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"textEditor_response": content}
