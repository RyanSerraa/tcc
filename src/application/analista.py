from src.domain.state import State


class Analista:
    def __init__(self, agent):
        self.analista = agent

    def respond(self, state: State):
        prompt = f'Pergunta: "{state.question}".\nDados: "{state.result}".\n'
        response = self.analista.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"analista_response": content}
