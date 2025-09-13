# agent_manager.py
from langgraph.graph import END, START, StateGraph

from src.application.run_query import RunQuery
from src.domain.state import State


class AgentManager:

    def __init__(
        self,
        connection,
        text_to_sql_agent,
        text_editor_agent,
        chart_editor_agent,
        web_search_agent,
        supervisor_agent,
        jornalista_agent,
        analista_agent,
        embeddings,
    ):
        self.connection = connection
        self.text_to_sql = text_to_sql_agent
        self.text_editor = text_editor_agent
        self.chart_editor = chart_editor_agent
        self.web_search = web_search_agent
        self.embeddings = embeddings
        self.run_query = RunQuery(connection).run_query
        self.supervisor = supervisor_agent
        self.jornalista = jornalista_agent
        self.analista = analista_agent
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
        self.workflow.add_node("run_query", self.run_query)
        self.workflow.add_node(
            "respondWithChart", lambda state: self.chart_editor.respond(state)
        )
        self.workflow.add_node(
            "respondWithText", lambda state: self.text_editor.respond(state)
        )

        self.workflow.add_edge(START, "supervisor")
        self.workflow.add_conditional_edges(
            "supervisor",
            self.verifySupervisorAnswer,
            {"Yes": "to_sql_query", "No": "searchWeb"},
        )
        self.workflow.add_edge("to_sql_query", "run_query")
        self.workflow.add_conditional_edges(
            "run_query",
            self.hasChart,
            {"Yes": "respondWithChart", "No": "respondWithText"},
        )
        self.workflow.add_edge("respondWithText", END)
        self.workflow.add_edge("respondWithChart", END)
        self.workflow.add_edge("searchWeb", END)

    def verifySupervisorAnswer(self, state: State):
        return "Yes" if state.get("isEUA") else "No"

    def hasChart(self, state: State):
        return "Yes" if "gráfico" in state.get("question", "").lower() else "No"
