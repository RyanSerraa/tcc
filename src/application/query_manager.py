# query_manager.py
from src.application.agent_orchestrator import AgentManager
from src.domain.state import State


class QueryManager:

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager

    def consultar_dados(self, question: str) -> dict:
        state = State(question=question)
        try:
            result = self.agent_manager.chain.invoke(state)
            return {
                "success": True,
                "text_response": result.get("redator_response", {}).get(
                    "final_textual_response" or result.get("searchWeb_response")
                ),
                "chart_response": result.get("redator_response", {}).get("chart")
                or result.get("result"),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
