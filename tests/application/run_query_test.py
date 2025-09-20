from unittest.mock import MagicMock

from src.application.run_query import RunQuery
from src.domain.state import State


def test_run_query_select():
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "state": "Texas"}]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    rq = RunQuery(mock_conn)
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="SELECT * FROM DLocalidade WHERE estado = 'Texas'",
        result="",
        gerente_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        searchWeb_response="",
        redator_response={},
    )
    result = rq.run_query(state)

    assert result == {"result": [{"id": 1, "state": "Texas"}]}
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM DLocalidade WHERE estado = 'Texas'"
    )
