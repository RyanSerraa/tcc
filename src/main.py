import json
import logging
from typing import Any, Dict

from config.config import Config
from src.application.agent_orchestrator import AgentManager
from src.application.insight_reasoner import InsightReasoner
from src.application.insight_drawer import InsightDrawer
from src.application.manager import Manager
from src.application.session_manager import SessionManager
from src.application.insight_editor import InsightEditor
from src.application.run_query import RunQuery
from src.application.supervisor import Supervisor
from src.application.insight_writer import InsightWriter
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

    def run(self):
        try:
            text_to_sql_agent = TextToSQL(Agents.load_agent(*self.config.text_to_sql))
            insight_writer_agent = InsightWriter(
                Agents.load_agent(*self.config.insight_writer)
            )
            insight_drawer_agent = InsightDrawer(
                Agents.load_agent(*self.config.insight_drawer)
            )
            web_researcher_agent = WebResearcher(
                Agents.load_agent(*self.config.web_researcher)
            )
            supervisor_agent = Supervisor(Agents.load_agent(*self.config.supervisor))
            manager_agent = Manager(Agents.load_agent(*self.config.manager))
            insight_reasoner_agent = InsightReasoner(
                Agents.load_agent(*self.config.insight_reasoner)
            )
            insight_editor_agent = InsightEditor(
                Agents.load_agent(*self.config.insight_editor)
            )

            logging.info("Todos os agentes carregados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao carregar agentes: {e}", exc_info=True)
            return

        schema_text: str = self.load_file("src/resources/schema.txt")

        embeddings = Embeddings()
        if self.config.db_url is None:
            logging.error("Database URL is not configured.")
            return
        db = DB(self.config.db_url)
        exemplary_data = db.getExemplaryData()
        run_query_agent = RunQuery(db)
        agent_manager = AgentManager(
            db=db,
            text_to_sql_agent=text_to_sql_agent,
            insight_writer_agent=insight_writer_agent,
            insight_drawer_agent=insight_drawer_agent,
            web_researcher_agent=web_researcher_agent,
            supervisor_agent=supervisor_agent,
            embeddings=embeddings,
            manager_agent=manager_agent,
            run_query_agent=run_query_agent,
            insight_reasoner_agent=insight_reasoner_agent,
            insight_editor_agent=insight_editor_agent,
        )

        query_manager = SessionManager(agent_manager=agent_manager)
        app = Index(
            query_manager=query_manager,
            schema_text=schema_text,
            exemplary_data=exemplary_data,
        )
        app.render()


if __name__ == "__main__":
    Main().run()
