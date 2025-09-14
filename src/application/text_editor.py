from src.domain.state import State


class TextEditor:
    def __init__(self, agent):
        self.text_editor = agent

    def respond(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\".\nDados: \"{state.get('result', [])}\".\n"
        response = self.text_editor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        # adiciona a resposta dentro do state
        state["answer"] = answer
        return state  # retorna o state completo
