from unittest.mock import MagicMock

from src.application.gerente import Gerente
from src.domain.state import State


def test_gerente_respond():
    mock_agent = MagicMock()
    mock_response_json = (
        '{"textEditor": "Sim", "chartEditor": "Não", "analista": "Sim"}'
    )
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_response_json))
    ]

    gerente = Gerente(mock_agent)

    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        gerente_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        searchWeb_response="",
        redator_response={},
    )

    result = gerente.choose_chain(state)
    expected_response = {
        "textEditor": "Sim",
        "chartEditor": "Não",
        "analista": "Sim",
    }

    assert result["gerente_decision"] == expected_response
    mock_agent.chat.completions.create.assert_called_once()
