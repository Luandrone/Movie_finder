import pytest
from unittest.mock import patch

from app.banco.conexao import obter_conexao


@patch('app.banco.conexao.psycopg.connect')
@patch('app.banco.conexao.load_dotenv')
def test_obter_conexao_com_configuracoes_ausentes(
    mock_load_dotenv,
    mock_connect,
    monkeypatch
):
    variaveis = [
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD'
    ]

    for variavel in variaveis:
        monkeypatch.delenv(variavel, raising=False)

    with pytest.raises(ValueError) as excecao_info:
        obter_conexao()

    assert 'DB_HOST' in str(excecao_info.value)
    assert 'DB_PASSWORD' in str(excecao_info.value)

    mock_connect.assert_not_called()