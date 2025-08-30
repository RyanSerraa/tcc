from src.domain.state import State


class WebSearch:
    def __init__(self, agent):
        self.web_search = agent

    def search(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\"."
        response = self.web_search.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = response.choices[0].message.content.strip() if response.choices else ""
        return {"answer": answer}
