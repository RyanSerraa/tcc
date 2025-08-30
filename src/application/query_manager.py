# query_manager.py
from src.application.agent_orchestrator import AgentManager


class QueryManager:

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager

    def consultar_dados(self, question: str) -> dict:
        try:
            result = self.agent_manager.chain.invoke({"question": question})
            return {
                "success": True,
                "answer": result.get("answer") or result.get("result"),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
