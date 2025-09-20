from src.domain.state import State


class TextEditor:
    def __init__(self, agent):
        self.text_editor = agent

    def respond(self, state: State):
        prompt = f'Pergunta: "{state.question}".\nDados: "{state.result}".\n'
        response = self.text_editor.chat.completions.create(
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
