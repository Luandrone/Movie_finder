import pytest
import requests.exceptions
from unittest.mock import patch, Mock

from app.api import fazer_requisicao
from app.excecoes import ErroApi
from tests.test_filme import mock_response


@patch('app.api.requests.get')
def test_fazer_requisicao_erro_conexao(mock_request_get):
    mock_request_get.side_effect = requests.exceptions.ConnectionError
    with pytest.raises(ErroApi) as excecao_info:
        fazer_requisicao('https://exemplo.com',{'Accept': 'application/json'})
    assert excecao_info.value.tipo == 'Problema de conexão'

@patch('app.api.requests.get')
def test_fazer_requisicao_http(mock_request_get):
    mock_request_get.side_effect = requests.exceptions.HTTPError
    with pytest.raises(ErroApi) as excecao_info:
        fazer_requisicao('https://exemplo.com',{'Accept': 'application/json'})
    assert excecao_info.value.tipo == 'Problema de Http'

@patch('app.api.requests.get')
def test_fazer_requisicao_sucesso(mock_request_get):
    mock_response = Mock()
    mock_request_get.return_value = mock_response
    response = fazer_requisicao('https://exemplo.com',{'Accept': 'application/json'})
    assert response is mock_response


