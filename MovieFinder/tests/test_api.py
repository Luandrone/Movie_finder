import pytest
import requests.exceptions
from unittest.mock import patch, Mock

from app.api import fazer_requisicao, buscar_detalhes, buscar_disponibilidade
from app.excecoes import ErroApi
from app.filme import Filme

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

@patch('app.api.fazer_requisicao')
def test_buscar_detalhes(mock_detalhes):
    dados_falsos = {'overview':'blablabla',
                    'runtime':210,
                    'poster_path':'blablabla',
                    'genres':[
                        {'name': 'Crime'},
                        {'name': 'Thriller'}]}
    mock_response = Mock()
    mock_response.json.return_value = dados_falsos
    mock_detalhes.return_value = mock_response
    filme1 = Filme()
    buscar_detalhes(filme1)

    assert filme1.sinopse == 'blablabla'
    assert filme1.duracao == 210
    assert filme1.poster == 'blablabla'
    assert filme1.generos == ['Crime', 'Thriller']

@patch('app.api.fazer_requisicao')
def test_buscar_disponibilidade(mock_disponibilidade):
    dados_falsos = {
        'results': {
            'BR': {
                'flatrate': [
                    {'provider_name': 'Netflix'}
                ],
                'rent': [
                    {'provider_name': 'Amazon Video'}
                ],
                'buy': [
                    {'provider_name': 'Google'}
                ]
            }
        }
    }
    mock_response = Mock()
    mock_response.json.return_value = dados_falsos
    mock_disponibilidade.return_value = mock_response
    filme1 = Filme()
    buscar_disponibilidade(filme1)

    assert filme1.disponibilidade == dados_falsos['results']['BR']

@patch('app.api.fazer_requisicao')
def test_buscar_disponibilidade_sem_brasil(mock_disponibilidade):
    dados_falsos = {
        'results': {}
    }
    mock_response = Mock()
    mock_response.json.return_value = dados_falsos
    mock_disponibilidade.return_value = mock_response
    filme1 = Filme()
    buscar_disponibilidade(filme1)

    assert filme1.disponibilidade == {}


