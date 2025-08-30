from unittest.mock import MagicMock

from src.application.run_query import RunQuery


def test_run_query_select():
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "state": "Texas"}]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    rq = RunQuery(mock_conn)
    result = rq.run_query({"query": "SELECT * FROM DLocalidade WHERE estado = 'Texas'"})

    assert result == {"result": [{"id": 1, "state": "Texas"}]}
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM DLocalidade WHERE estado = 'Texas'"
    )
