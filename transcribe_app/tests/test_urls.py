from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_api_transcriptions(api_client):
    response = api_client.get('/api/transcriptions/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_personalities(api_client):
    response = api_client.get('/api/personalities/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_cities(api_client):
    response = api_client.get('/api/cities/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_countries(api_client):
    response = api_client.get('/api/countries/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_textblock(api_client):
    response = api_client.get('/api/textblock/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_keywords(api_client):
    response = api_client.get('/api/keywords/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_transcriptions_save(api_client):
    response = api_client.get('/api/transcriptions_save/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")


@pytest.mark.django_db
def test_api_partial(api_client):
    response = api_client.get('/api/partial/')
    assert response.status_code == HTTPStatus.OK, (
        f"Ошибка {response.status_code} при открытиии запроса")
