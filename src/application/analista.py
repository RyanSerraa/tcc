from src.domain.state import State

class Analista:

    def __init__(self, agente):
        self.analista_agent = agente

    def respond(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\".\nDados: \"{state['result']}\".\n"
        response = self.analista_agent.chat.completions.create(
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