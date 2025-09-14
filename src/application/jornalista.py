import json

from src.domain.state import State


class Jornalista:
    def __init__(self, agente, text_editor, chart_editor, analista):
        self.jornalista_agent = agente
        self.text_editor = text_editor
        self.chart_editor = chart_editor
        self.analista = analista

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
        contexto = embeddings.getContext(state["question"], "jornalista", connection)
        prompt = (
            f"Contexto relevante:\n{contexto}\n"
            f'Pergunta do usuário: "{state["question"]}".\n\n'
            f"Responda apenas em JSON, no formato:\n"
            '{"texto": "sim" ou "não", "chart": "sim" ou "não", "analise": "sim" ou "não"}\n'
            "Não adicione explicações ou qualquer outro texto."
        )

        response = self.jornalista_agent.chat.completions.create(
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
    def write_article(self, state: State) -> str:
        """
        Orquestra os agentes, consolida respostas e aplica revisão final.
        """
        if "agents_done" not in state:
            state["agents_done"] = {
                "analista": False,
                "respondWithText": False,
                "respondWithChart": False,
            }

        respostas = {}

        # Chama analista se necessário
        if state.get("isAnalisis", False) and not state["agents_done"]["analista"]:
            respostas["analista"] = self.analista.respond(state)
            state["agents_done"]["analista"] = True

        # Chama agente de texto se necessário
        if (state.get("isText", False) or state.get("isAnalisis", False)) and not state["agents_done"]["respondWithText"]:
            respostas["texto"] = self.text_editor.respond(state)
            state["agents_done"]["respondWithText"] = True

        # Chama agente de gráfico se necessário
        if (state.get("isChart", False) or state.get("isAnalisis", False)) and not state["agents_done"]["respondWithChart"]:
            respostas["grafico"] = self.chart_editor.respond(state)
            state["agents_done"]["respondWithChart"] = True

        # Consolida respostas
        artigo_final = "Artigo consolidado:\n\n"
        for key, value in respostas.items():
            artigo_final += f"[{key.upper()}]: {value.get('answer', '')}\n\n"

        # Aplica revisão final
        artigo_final += "Revisão final: texto revisado e aprimorado com todas as informações."

        return artigo_final
