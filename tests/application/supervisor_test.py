from unittest.mock import MagicMock, patch

import pandas as pd

from src.application.supervisor import Supervisor
from src.domain.state import State


def test_supervisor_choose_chain_yes():
    # Mock do agente
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Sim"))
    ]

    # Mock do embeddings
    mock_embeddings = MagicMock()
    mock_embeddings.getContext.return_value = "contexto relevante"

    mock_db = MagicMock()
    mock_db.execute_query.return_value = [{"nome": "Finance"}]

    # Cria um DataFrame simulado
    df_mock = pd.DataFrame({0: ["Finance"]})

    # Patch do pandas read_csv para retornar DataFrame
    with patch("pandas.read_csv", return_value=df_mock):
        supervisor = Supervisor(mock_agent)

    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        manager_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        web_researcher_response="",
        redator_response={},
    )

    result = supervisor.choose_chain(state, mock_embeddings, mock_db)

    assert result["isEUA"] is True
    mock_agent.chat.completions.create.assert_called_once()
    mock_embeddings.getContext.assert_called_once_with(
        state.question, "supervisor", mock_db
    )
