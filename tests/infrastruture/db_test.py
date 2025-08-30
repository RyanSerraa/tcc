# tests/infrastructure/db_test.py
from unittest.mock import MagicMock, patch

import psycopg2
import pytest

from src.infrastructure.db import db


def test_get_connection_success():
    mock_conn = MagicMock()
    with patch(
        "src.infrastructure.db.psycopg2.connect", return_value=mock_conn
    ) as mock_connect:
        d = db()
        conn = d.get_connection("postgres://fake_url")
        mock_connect.assert_called_once_with(
            "postgres://fake_url", cursor_factory=psycopg2.extras.DictCursor
        )
        assert conn == mock_conn


def test_get_connection_exception():
    with patch(
        "src.infrastructure.db.psycopg2.connect",
        side_effect=psycopg2.OperationalError("Erro de conexão"),
    ):
        d = db()
        with pytest.raises(psycopg2.OperationalError, match="Erro de conexão"):
            d.get_connection("postgres://fake_url")
