from unittest.mock import MagicMock

from src.application.manager import Manager
from src.domain.state import State


def test_gerente_respond():
    mock_agent = MagicMock()
    mock_response_json = (
        '{"textEditor": "Sim", "chartEditor": "Não", "analista": "Sim"}'
    )
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_response_json))
    ]

    manager = Manager(mock_agent)

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

    result = manager.choose_chain(state)
    expected_response = {
        "textEditor": "Sim",
        "chartEditor": "Não",
        "analista": "Sim",
    }

    assert result["manager_decision"] == expected_response
    mock_agent.chat.completions.create.assert_called_once()
