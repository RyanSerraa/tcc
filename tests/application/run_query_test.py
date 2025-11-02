from unittest.mock import MagicMock

from src.application.run_query import RunQuery
from src.domain.state import State


def test_run_query_select():
    mock_db = MagicMock()
    mock_db.execute_query.return_value = [{"id": 1, "state": "Texas"}]
    rq = RunQuery(mock_db)
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="SELECT * FROM DLocalidade WHERE estado = 'Texas'",
        result="",
        manager_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        web_researcher_response="",
        redator_response={},
    )
    result = rq.run_query(state)

    assert result == {"result": [{"id": 1, "state": "Texas"}]}
    mock_db.execute_query.assert_called_once_with(
        "SELECT * FROM DLocalidade WHERE estado = 'Texas'"
    )
