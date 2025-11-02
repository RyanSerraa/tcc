# tests/infrastructure/embeddings_test.py
from unittest.mock import MagicMock, patch

from src.infrastructure.embeddings import Embeddings


def test_embed_query_called():
    mock_model = MagicMock()
    mock_model.embed_query.return_value = [0.1, 0.2, 0.3]

    # Mocka a classe HuggingFaceEmbeddings para que Embeddings use o mock
    with patch(
        "src.infrastructure.embeddings.HuggingFaceEmbeddings", return_value=mock_model
    ):
        emb = Embeddings()  # vai usar mock_model
        result = emb.embed_query("Qual a principal causa de morte?")
        mock_model.embed_query.assert_called_once_with(
            "Qual a principal causa de morte?"
        )
        assert result == [0.1, 0.2, 0.3]


def test_getContext_returns_formatted_string():
    mock_model = MagicMock()
    mock_model.embed_query.return_value = [0.1, 0.2, 0.3]

    with patch(
        "src.infrastructure.embeddings.HuggingFaceEmbeddings", return_value=mock_model
    ):
        emb = Embeddings()

        mock_db = MagicMock()
        # Retorna tuplas (pergunta, resposta) - corresponde à implementação atual
        mock_db.execute_query.return_value = [
            ("P1", "R1"),
            ("P2", "R2"),
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
