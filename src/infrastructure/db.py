import psycopg2
from psycopg2.extras import DictCursor


class db:
    def get_connection(self, db_url: str):
        return psycopg2.connect(db_url, cursor_factory=DictCursor)
