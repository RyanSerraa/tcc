import re

from psycopg2.extras import DictCursor


class RunQuery:
    def __init__(self, connection):
        self.connection = connection

    def run_query(self, state: dict) -> dict:
        print("Running query:", state.get("query"))
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                query = state["query"].strip()  # pega do estado
                cursor.execute(query)
                if re.match(r"^(select|with)\b", query, re.IGNORECASE):
                    state["result"] = [dict(row) for row in cursor.fetchall()]
                else:
                    self.connection.commit()
                    state["affected_rows"] = cursor.rowcount
        except Exception as e:
            state["status"] = "error"
            state["message"] = str(e)
        return state
