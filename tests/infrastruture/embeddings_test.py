# tests/infrastructure/embeddings_test.py
from unittest.mock import MagicMock, patch

from src.infrastructure.embeddings import Embeddings


def test_embed_query_called():
    mock_model = MagicMock()
    mock_model.encode.return_value = [0.1, 0.2, 0.3]

    # Mocka a classe SentenceTransformer para que Embeddings use o mock
    with patch(
        "src.infrastructure.embeddings.SentenceTransformer", return_value=mock_model
    ):
        emb = Embeddings()  # vai usar mock_model
        result = emb.embed_query("Qual a principal causa de morte?")
        mock_model.encode.assert_called_once_with("Qual a principal causa de morte?")
        assert result == [0.1, 0.2, 0.3]


def test_getContext_returns_formatted_string():
    mock_model = MagicMock()

    class MockArray:
        def __init__(self, arr):
            self._arr = arr

        def tolist(self):
            return self._arr

    mock_model.encode.return_value = MockArray([0.1, 0.2, 0.3])

    with patch(
        "src.infrastructure.embeddings.SentenceTransformer", return_value=mock_model
    ):
        emb = Embeddings()

        mock_db = MagicMock()
        mock_db.execute_query.return_value = [
            {"pergunta": "P1", "resposta": "R1"},
            {"pergunta": "P2", "resposta": "R2"},
        ]

        contexto = emb.getContext(
            "Qual a principal causa de morte?", "text_to_sql", mock_db
        )
        print(contexto)

        mock_db.execute_query.assert_called_once()
        assert "1. Pergunta: P1" in contexto
        assert "2. Pergunta: P2" in contexto
        assert "Resposta: R1" in contexto
        assert "Resposta: R2" in contexto
