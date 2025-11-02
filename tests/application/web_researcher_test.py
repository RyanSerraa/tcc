from unittest.mock import MagicMock

from src.application.web_researcher import WebResearcher
from src.domain.state import State


def test_web_search_respond():
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    web_search = WebResearcher(mock_agent)

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

    result = web_search.search(state)

    assert result["web_researcher_response"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
