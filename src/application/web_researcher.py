from src.domain.state import State


class WebResearcher:
    def __init__(self, agent):
        self.web_researcher = agent

    def search(self, state: State):
        prompt = f'Pergunta: "{state.question}".'
        response = self.web_researcher.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        return {"web_researcher_response": content}
