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
        self.insight_writer = (
            os.getenv("INSIGHT_WRITER_AGENT_ENDPOINT"),
            os.getenv("INSIGHT_WRITER_API_KEY"),
        )
        self.insight_drawer = (
            os.getenv("INSIGHT_DRAWER_AGENT_ENDPOINT"),
            os.getenv("INSIGHT_DRAWER_API_KEY"),
        )
        self.web_researcher = (
            os.getenv("WEB_RESEARCHER_AGENT_ENDPOINT"),
            os.getenv("WEB_RESEARCHER_API_KEY"),
        )
        self.supervisor = (
            os.getenv("SUPERVISOR_AGENT_ENDPOINT"),
            os.getenv("SUPERVISOR_API_KEY"),
        )
        self.manager = (
            os.getenv("MANAGER_AGENT_ENDPOINT"),
            os.getenv("MANAGER_API_KEY"),
        )
        self.insight_reasoner = (
            os.getenv("INSIGHT_REASONER_AGENT_ENDPOINT"),
            os.getenv("INSIGHT_REASONER_API_KEY"),
        )
        self.insight_editor = (
            os.getenv("INSIGHT_EDITOR_AGENT_ENDPOINT"),
            os.getenv("INSIGHT_EDITOR_API_KEY"),
        )
