import json
import logging
from typing import Any

import streamlit as st

from config.config import Config
from src.application.agent_orchestrator import AgentManager
from src.application.insight_drawer import InsightDrawer
from src.application.insight_editor import InsightEditor
from src.application.insight_reasoner import InsightReasoner
from src.application.insight_writer import InsightWriter
from src.application.manager import Manager
from src.application.run_query import RunQuery
from src.application.session_manager import SessionManager
from src.application.supervisor import Supervisor
from src.application.text_to_sql import TextToSQL
from src.application.web_researcher import WebResearcher
from src.infrastructure.ai_agents import Agents
from src.infrastructure.db import DB
from src.infrastructure.embeddings import Embeddings
from src.interfaces.ui.stremlit_app import Index


class Main:
    def __init__(self):
        self.config = Config()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    @staticmethod
    def load_file(file: str, type: str = "text") -> Any:
        with open(file, "r") as f:
            if type == "json":
                return json.load(f)
            return f.read()

    @st.cache_resource(show_spinner=False)
    def initialize_embeddings(_self):
        return Embeddings()

    @st.cache_resource(show_spinner=False)
    def initialize_db(_self):
        if _self.config.db_url is None:
            logging.error("Database URL is not configured.")
            return None
        return DB(_self.config.db_url)

    @st.cache_resource(show_spinner=False)
    def initialize_exemplary_data(_self, _db):
        return _db.getExemplaryData()

    @st.cache_resource(show_spinner=False)
    def initialize_agents(_self, _db, _embeddings):
        try:
            text_to_sql_agent = TextToSQL(Agents.load_agent(*_self.config.text_to_sql))
            insight_writer_agent = InsightWriter(
                Agents.load_agent(*_self.config.insight_writer)
            )
            insight_drawer_agent = InsightDrawer(
                Agents.load_agent(*_self.config.insight_drawer)
            )
            web_researcher_agent = WebResearcher(
                Agents.load_agent(*_self.config.web_researcher)
            )
            supervisor_agent = Supervisor(Agents.load_agent(*_self.config.supervisor))
            manager_agent = Manager(Agents.load_agent(*_self.config.manager))
            insight_reasoner_agent = InsightReasoner(
                Agents.load_agent(*_self.config.insight_reasoner)
            )
            insight_editor_agent = InsightEditor(
                Agents.load_agent(*_self.config.insight_editor)
            )

            run_query_agent = RunQuery(_db)

            agent_manager = AgentManager(
                db=_db,
                text_to_sql_agent=text_to_sql_agent,
                insight_writer_agent=insight_writer_agent,
                insight_drawer_agent=insight_drawer_agent,
                web_researcher_agent=web_researcher_agent,
                supervisor_agent=supervisor_agent,
                embeddings=_embeddings,
                manager_agent=manager_agent,
                run_query_agent=run_query_agent,
                insight_reasoner_agent=insight_reasoner_agent,
                insight_editor_agent=insight_editor_agent,
            )

            logging.info("Todos os agentes carregados com sucesso")
            return agent_manager
        except Exception as e:
            logging.error(f"Erro ao carregar agentes: {e}", exc_info=True)
            return None

    @st.cache_resource(show_spinner=False)
    def initialize_query_manager(_self, _agent_manager: AgentManager):
        return SessionManager(_agent_manager)

    def run(self):
        embeddings = self.initialize_embeddings()
        db = self.initialize_db()
        if db is None:
            return
        exemplary_data = self.initialize_exemplary_data(db)
        schema_text: str = self.load_file("src/resources/schema.txt")
        agent_manager = self.initialize_agents(db, embeddings)
        query_manager = self.initialize_query_manager(agent_manager)
        app = Index(
            query_manager=query_manager,
            schema_text=schema_text,
            exemplary_data=exemplary_data,
        )
        app.render()


if __name__ == "__main__":
    Main().run()
