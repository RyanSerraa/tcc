from psycopg2.extras import DictCursor
import re


class RunQuery:
    def __init__(self, connection):
        self.connection = connection

    def run_query(self, sql_query: dict):
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                query = sql_query["query"].strip()
                cursor.execute(query)
                if re.match(r"^(select|with)\b", query, re.IGNORECASE):
                    rows = cursor.fetchall()
                    return {"result": [dict(row) for row in rows]}
                else:
                    self.connection.commit()
                    return {"affected_rows": cursor.rowcount}
        except Exception as e:
            return {"status": "error", "message": str(e)}
