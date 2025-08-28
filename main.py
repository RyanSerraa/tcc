# main.py
import os
from dotenv import load_dotenv
from infra.ai_agents import Agents
from infra.db import db
from infra.embeddings import Embeddings
from model.agent_manager import AgentManager
from controller.query_manager import QueryManager
from view.index import Index


class Main:
    def __init__(self):
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL")
        self.text_to_sql = os.getenv("TEXT_TO_SQL_AGENT_ENDPOINT")
        self.text_to_sql_api_key = os.getenv("TEXT_TO_SQL_API_KEY")
        self.text_editor_model = os.getenv("TEXT_EDITOR_AGENT_ENDPOINT")
        self.text_editor_model_api_key = os.getenv("TEXT_EDITOR_API_KEY")
        self.chart_editor_model = os.getenv("CHART_EDITOR_AGENT_ENDPOINT")
        self.chart_editor_model_api_key = os.getenv("CHART_EDITOR_API_KEY")
        self.web_search_model = os.getenv("WEB_SEARCH_AGENT_ENDPOINT")
        self.web_search_model_api_key = os.getenv("WEB_SEARCH_API_KEY")
        self.supervisor_model = os.getenv("SUPERVISOR_AGENT_ENDPOINT")
        self.supervisor_model_api_key = os.getenv("SUPERVISOR_API_KEY")

    @staticmethod
    def load_file(file):
        with open(file, "r") as f:
            return f.read()
    def run(self):
        # Carregar agentes
        try:
            text_to_sql_agent = Agents.load_agent(
                self.text_to_sql, self.text_to_sql_api_key
            )
            text_editor_agent = Agents.load_agent(
                self.text_editor_model, self.text_editor_model_api_key
            )
            chart_editor_agent = Agents.load_agent(
                self.chart_editor_model, self.chart_editor_model_api_key
            )
            web_search_agent = Agents.load_agent(
                self.web_search_model, self.web_search_model_api_key
            )
            supervisor_agent = Agents.load_agent(
                self.supervisor_model, self.supervisor_model_api_key
            )
            print("Todos os agentes carregados com sucesso")
        except Exception as e:
            print("Erro ao carregar agentes:", e)
            return
        schema_text = self.load_file("resources/schema.txt")
        # Inicializar embeddings
        embeddings = Embeddings().load_model()

        # Conectar ao banco e criar managers
        connection = None
        try:
            connection = db.get_connection(self.db_url)
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
            print("Erro ao conectar ao banco:", e)
        finally:
            if connection:
                connection.close()
                print("Conexão com o banco encerrada")


if __name__ == "__main__":
    Main().run()
