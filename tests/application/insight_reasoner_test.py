from unittest.mock import MagicMock

from src.application.insight_reasoner import InsightReasoner
from src.domain.state import State


def test_analista_respond():
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    insight_reasoner = InsightReasoner(mock_agent)

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

    result = insight_reasoner.respond(state)

    assert result["analista_response"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
