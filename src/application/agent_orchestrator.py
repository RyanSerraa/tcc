# agent_manager.py
from langgraph.graph import END, START, StateGraph

from src.domain.state import State


class AgentManager:

    def __init__(
        self,
        connection,
        text_to_sql_agent,
        text_editor_agent,
        chart_editor_agent,
        web_search_agent,
        run_query_agent,
        supervisor_agent,
        gerente_agent,
        embeddings,
        analista_agent,
        redator_agent,
    ):
        self.connection = connection
        self.text_to_sql = text_to_sql_agent
        self.text_editor = text_editor_agent
        self.chart_editor = chart_editor_agent
        self.gerente = gerente_agent
        self.web_search = web_search_agent
        self.embeddings = embeddings
        self.run_query = run_query_agent
        self.supervisor = supervisor_agent
        self.analista = analista_agent
        self.redator = redator_agent
        self.workflow = StateGraph(State)
        self._build_workflow()
        self.chain = self.workflow.compile()

    def _build_workflow(self):
        self.workflow.add_node(
            "supervisor",
            lambda state: self.supervisor.choose_chain(
                state, self.embeddings, self.connection
            ),
        )
        self.workflow.add_node("searchWeb", lambda state: self.web_search.search(state))
        self.workflow.add_node(
            "to_sql_query",
            lambda state: self.text_to_sql.to_sql_query(
                state, self.embeddings, self.connection
            ),
        )
        self.workflow.add_node(
            "gerente", lambda state: self.gerente.choose_chain(state)
        )
        self.workflow.add_node(
            "run_query", lambda state: self.run_query.run_query(state)
        )
        self.workflow.add_node(
            "chartEditor", lambda state: self.chart_editor.respond(state)
        )
        self.workflow.add_node(
            "textEditor", lambda state: self.text_editor.respond(state)
        )
        self.workflow.add_node("analista", lambda state: self.analista.respond(state))
        self.workflow.add_node("redator", lambda state: self.redator.respond(state))

        self.workflow.add_edge(START, "supervisor")
        self.workflow.add_conditional_edges(
            "supervisor",
            self.verifySupervisorResponse,
            {"Sim": "to_sql_query", "Não": "searchWeb"},
        )
        self.workflow.add_edge("to_sql_query", "run_query")
        self.workflow.add_edge("run_query", "gerente")
        self.workflow.add_conditional_edges(
            "gerente",
            self.verifyGerenteResponse,
            {
                "textEditor": "textEditor",
                "chartEditor": "chartEditor",
                "analista": "analista",
            },
        )

        self.workflow.add_edge("textEditor", "redator")
        self.workflow.add_edge("chartEditor", "redator")
        self.workflow.add_edge("analista", "redator")
        # self.workflow.add_edge("redator", END)
        self.workflow.add_conditional_edges(
            "redator",
            self.verifyRedatorResponse,
            {"refazerGrafico": "chartEditor", None: END},
        )
        self.workflow.add_edge("searchWeb", END)

    def verifySupervisorResponse(self, state: State):
        return "Sim" if state.isEUA else "Não"

    def verifyGerenteResponse(self, state: State):
        decision = state.gerente_decision
        outputs = []

        if decision.get("textEditor") == "sim":
            outputs.append("textEditor")
        if decision.get("chartEditor") == "sim":
            outputs.append("chartEditor")
        if decision.get("analista") == "sim":
            outputs.append("analista")

        return outputs

    def verifyRedatorResponse(self, state: State):
        decision = state.redator_response
        if decision.get("redoChart") == True:
            return "refazerGrafico"

        return None
