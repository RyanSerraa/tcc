from unittest.mock import MagicMock


from src.application.query_manager import QueryManager


def test_consultar_dados_sucesso():
    # Mock do AgentManager
    mock_agent_manager = MagicMock()
    mock_agent_manager.chain.invoke.return_value = {"answer": "Resultado simulado"}

    qm = QueryManager(mock_agent_manager)
    result = qm.consultar_dados(
        "Qual a principal causa de morte por arma de fogo na Califórnia?"
    )

    assert result == {"success": True, "answer": "Resultado simulado"}
    mock_agent_manager.chain.invoke.assert_called_once_with(
        {"question": "Qual a principal causa de morte por arma de fogo na Califórnia?"}
    )


def test_consultar_dados_erro():
    mock_agent_manager = MagicMock()
    mock_agent_manager.chain.invoke.side_effect = Exception("Falha na chain")

    qm = QueryManager(mock_agent_manager)
    result = qm.consultar_dados("Pergunta qualquer")

    assert result == {"success": False, "error": "Falha na chain"}
