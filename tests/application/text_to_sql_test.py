from unittest.mock import MagicMock

from src.application.text_to_sql import TextToSQL
from src.domain.state import State


def test_text_to_sql_query():
    # Mock do agente
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="SELECT * FROM tabela;"))
    ]

    # Mock do embeddings
    mock_embeddings = MagicMock()
    mock_embeddings.getContext.return_value = "contexto relevante"

    # Mock da conexão (pode ser None)
    mock_db = MagicMock()
    mock_db.execute_query.return_value = []

    text_to_sql = TextToSQL(mock_agent)

    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        manager_decision={},
        insight_writer_response="",
        insight_drawer_response="",
        insight_reasoner_response="",
        web_researcher_response="",
        insight_editor_response={},
    )

    result = text_to_sql.to_sql_query(state, mock_embeddings, mock_db)

    assert result["query"] == "SELECT * FROM tabela;"
    mock_agent.chat.completions.create.assert_called_once()
    mock_embeddings.getContext.assert_called_once_with(
        state.question, "text_to_sql", mock_db
    )
