import json

from src.domain.state import State


class Gerente:
    def __init__(self, agente):
        self.gerente_agent = agente

    @staticmethod
    def parse_resposta(resposta_texto: str) -> dict:
        """Transforma a resposta JSON do agente em dicionário."""
        try:
            return json.loads(resposta_texto)
        except json.JSONDecodeError:
            return {"texto": "não", "chart": "não", "analise": "não"}

    @staticmethod
    def is_text(respostas: dict) -> bool:
        """Verifica se a resposta indica que deve gerar texto."""
        return respostas.get("texto", "").lower() == "sim"

    @staticmethod
    def is_chart(respostas: dict) -> bool:
        """Verifica se a resposta indica que deve gerar gráfico."""
        return respostas.get("chart", "").lower() == "sim"

    @staticmethod
    def is_analisis(respostas: dict) -> bool:
        """Verifica se a resposta indica que deve gerar análise."""
        return respostas.get("analise", "").lower() == "sim"

    def choose_chain(self, state: State, embeddings, connection) -> dict:
        """Orquestra a chamada ao agente e processa as respostas."""
        contexto = embeddings.getContext(state["question"], "gerente", connection)
        prompt = (
            f"Contexto relevante:\n{contexto}\n"
            f'Pergunta do usuário: "{state["question"]}".\n\n'
            f"Responda apenas em JSON, no formato:\n"
            '{"texto": "sim" ou "não", "chart": "sim" ou "não", "analise": "sim" ou "não"}\n'
            "Não adicione explicações ou qualquer outro texto."
        )

        response = self.gerente_agent.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )

        resposta_texto = (
            response.choices[0].message.content.strip() if response.choices else "{}"
        )
        respostas = self.parse_resposta(resposta_texto)

        return {
            "isText": self.is_text(respostas),
            "isChart": self.is_chart(respostas),
            "isAnalisis": self.is_analisis(respostas),
        }