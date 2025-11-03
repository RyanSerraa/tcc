# agent_manager.py
from langgraph.graph import END, START, StateGraph

from src.domain.state import State
from src.infrastructure.db import DB


class AgentManager:

    def __init__(
        self,
        db: DB,
        text_to_sql_agent,
        insight_writer_agent,
        insight_drawer_agent,
        web_researcher_agent,
        run_query_agent,
        supervisor_agent,
        manager_agent,
        embeddings,
        insight_reasoner_agent,
        insight_editor_agent,
    ):
        self.db = db
        self.text_to_sql = text_to_sql_agent
        self.insight_writer = insight_writer_agent
        self.insight_drawer = insight_drawer_agent
        self.manager = manager_agent
        self.web_researcher = web_researcher_agent
        self.embeddings = embeddings
        self.run_query = run_query_agent
        self.supervisor = supervisor_agent
        self.insight_reasoner = insight_reasoner_agent
        self.insight_editor = insight_editor_agent
        self.workflow = StateGraph(State)
        self._build_workflow()
        self.chain = self.workflow.compile()

    def _build_workflow(self):
        self.workflow.add_node(
            "supervisor",
            lambda state: self.supervisor.choose_chain(state, self.embeddings, self.db),
        )
        self.workflow.add_node(
            "web_researcher", lambda state: self.web_researcher.search(state)
        )
        self.workflow.add_node(
            "to_sql_query",
            lambda state: self.text_to_sql.to_sql_query(
                state, self.embeddings, self.db
            ),
        )
        self.workflow.add_node(
            "manager", lambda state: self.manager.choose_chain(state)
        )
        self.workflow.add_node(
            "run_query", lambda state: self.run_query.run_query(state)
        )
        self.workflow.add_node(
            "insight_drawer", lambda state: self.insight_drawer.respond(state)
        )
        self.workflow.add_node(
            "insight_writer", lambda state: self.insight_writer.respond(state)
        )
        self.workflow.add_node(
            "insight_reasoner", lambda state: self.insight_reasoner.respond(state)
        )
        self.workflow.add_node(
            "insight_editor", lambda state: self.insight_editor.respond(state)
        )

        self.workflow.add_edge(START, "supervisor")
        self.workflow.add_conditional_edges(
            "supervisor",
            self.verifySupervisorResponse,
            {"Yes": "to_sql_query", "No": "web_researcher"},
        )
        self.workflow.add_edge("to_sql_query", "run_query")
        self.workflow.add_edge("run_query", "manager")
        self.workflow.add_conditional_edges(
            "manager",
            self.verifyManagerResponse,
            {
                "insight_writer": "insight_writer",
                "insight_drawer": "insight_drawer",
                "insight_reasoner": "insight_reasoner",
            },
        )

        self.workflow.add_edge("insight_writer", "insight_editor")
        self.workflow.add_edge("insight_drawer", "insight_editor")
        self.workflow.add_edge("insight_reasoner", "insight_editor")
        self.workflow.add_conditional_edges(
            "insight_editor",
            self.verifyInsightEditorResponse,
            {"redoChart": "insight_drawer", None: END},
        )
        self.workflow.add_edge("web_researcher", END)

    def verifySupervisorResponse(self, state: State):
        return "Yes" if state.isEUA else "No"

    def verifyManagerResponse(self, state: State):
        decision = state.manager_decision
        outputs = []

        if decision.get("insightWriter") == "yes":
            outputs.append("insight_writer")
        if decision.get("insightDrawer") == "yes":
            outputs.append("insight_drawer")
        if decision.get("insightReasoner") == "yes":
            outputs.append("insight_reasoner")

        return outputs

    def verifyInsightEditorResponse(self, state: State):
        decision = state.insight_editor_response
        if decision.get("redoChart"):
            return "redoChart"

        return None
