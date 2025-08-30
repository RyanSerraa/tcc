from unittest.mock import MagicMock


from src.application.chart_editor import ChartEditor
from src.domain.state import State


def test_chart_editor_respond():
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    chart_editor = ChartEditor(mock_agent)

    state = State(
        {
            "question": "Qual é a população da Califórnia?",
            "isEUA": True,
            "query": "",
            "result": "População: 39 milhões",
            "answer": "",
        }
    )

    result = chart_editor.respond(state)

    assert result["answer"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
