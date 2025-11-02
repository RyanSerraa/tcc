import re

from src.domain.state import State
from src.infrastructure.db import DB


class RunQuery:
    def __init__(self, db: DB):
        self.db = db

    def run_query(self, state: State):
        try:
            query = state.query.strip()
            if re.match(r"^(select|with)\b", query, re.IGNORECASE):
                result = self.db.execute_query(query)
                return {"result": result}
            else:
                return {
                    "status": "error",
                    "message": "Only SELECT or CTE queries are allowed.",
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
