# src/infrastructure/config.py
import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL")
        self.text_to_sql = (
            os.getenv("TEXT_TO_SQL_AGENT_ENDPOINT"),
            os.getenv("TEXT_TO_SQL_API_KEY"),
        )
        self.text_editor = (
            os.getenv("TEXT_EDITOR_AGENT_ENDPOINT"),
            os.getenv("TEXT_EDITOR_API_KEY"),
        )
        self.chart_editor = (
            os.getenv("CHART_EDITOR_AGENT_ENDPOINT"),
            os.getenv("CHART_EDITOR_API_KEY"),
        )
        self.web_search = (
            os.getenv("WEB_SEARCH_AGENT_ENDPOINT"),
            os.getenv("WEB_SEARCH_API_KEY"),
        )
        self.supervisor = (
            os.getenv("SUPERVISOR_AGENT_ENDPOINT"),
            os.getenv("SUPERVISOR_API_KEY"),
        )
        self.gerente = (
            os.getenv("GERENTE_AGENT_ENDPOINT"),
            os.getenv("GERENTE_API_KEY"),
        )
        self.analista = (
            os.getenv("ANALISTA_AGENT_ENDPOINT"),
            os.getenv("ANALISTA_API_KEY"),
        )
        self.redator = (
            os.getenv("REDATOR_AGENT_ENDPOINT"),
            os.getenv("REDATOR_API_KEY"),
        )
