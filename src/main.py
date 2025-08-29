import logging
from src.infrastructure.ai_agents import Agents
from src.infrastructure.db import db
from src.infrastructure.embeddings import Embeddings
from src.domain.agent_manager import AgentManager
from src.application.query_manager import QueryManager
from src.interfaces.ui import Index
from config.config import Config


class Main:
    def __init__(self):
        self.config = Config()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    @staticmethod
    def load_file(file):
        with open(file, "r") as f:
            return f.read()

    def run(self):
        # Carregar agentes
        try:
            text_to_sql_agent = Agents.load_agent(*self.config.text_to_sql)
            text_editor_agent = Agents.load_agent(*self.config.text_editor)
            chart_editor_agent = Agents.load_agent(*self.config.chart_editor)
            web_search_agent = Agents.load_agent(*self.config.web_search)
            supervisor_agent = Agents.load_agent(*self.config.supervisor)
            logging.info("Todos os agentes carregados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao carregar agentes: {e}", exc_info=True)
            return

        schema_text = self.load_file("resources/schema.txt")

        # Inicializar embeddings
        embeddings = Embeddings().load_model()

        # Conectar ao banco e criar managers
        connection = None
        try:
            connection = db.get_connection(self.config.db_url)
            agent_manager = AgentManager(
                connection=connection,
                text_to_sql_agent=text_to_sql_agent,
                text_editor_agent=text_editor_agent,
                chart_editor_agent=chart_editor_agent,
                web_search_agent=web_search_agent,
                supervisor_agent=supervisor_agent,
                embeddings_model=embeddings,
            )

            query_manager = QueryManager(agent_manager=agent_manager)
            app = Index(query_manager=query_manager, schema_text=schema_text)
            app.render()
        except Exception as e:
            logging.error(f"Erro ao conectar ao banco: {e}", exc_info=True)
        finally:
            if connection:
                connection.close()
                logging.info("Conexão com o banco encerrada")


if __name__ == "__main__":
    Main().run()
