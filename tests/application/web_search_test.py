from unittest.mock import MagicMock


from src.application.web_search import WebSearch
from src.domain.state import State


def test_web_search_respond():
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    web_search = WebSearch(mock_agent)

    state = State(
        {
            "question": "Qual é a capital da Califórnia?",
            "isEUA": True,
            "query": "",
            "result": "",
            "answer": "",
        }
    )

    result = web_search.search(state)

    assert result["answer"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
