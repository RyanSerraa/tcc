from unittest.mock import MagicMock

from src.application.text_to_sql import TextToSQL
from src.domain.state import State


def test_text_to_sql_query():
    # Mock do agente
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="```sql\nSELECT * FROM tabela;\n```"))
    ]

    # Mock do embeddings
    mock_embeddings = MagicMock()
    mock_embeddings.getContext.return_value = "contexto relevante"

    # Mock da conexão (pode ser None)
    mock_connection = None

    text_to_sql = TextToSQL(mock_agent)

    state = State(
        {
            "question": "Liste todos os usuários em gráfico",
            "isEUA": True,
            "query": "",
            "result": "",
            "answer": "",
        }
    )

    result = text_to_sql.to_sql_query(state, mock_embeddings, mock_connection)

    assert result["query"] == "SELECT * FROM tabela;"
    mock_agent.chat.completions.create.assert_called_once()
    mock_embeddings.getContext.assert_called_once_with(
        state["question"], "text_to_sql", mock_connection
    )
