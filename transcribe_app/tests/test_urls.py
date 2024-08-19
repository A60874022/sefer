from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_api_transcriptions(api_client):
    """Тест для проверки доступности эндпоинта "/api/transcriptions/"."""
    response = api_client.get("/api/transcriptions/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_personalities(api_client):
    """Тест для проверки доступности эндпоинта "/api/personalities/"."""
    response = api_client.get("/api/personalities/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_cities(api_client):
    """Тест для проверки доступности эндпоинта "/api/cities/"."""
    response = api_client.get("/api/cities/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_countries(api_client):
    """Тест для проверки доступности эндпоинта "/api/countries/"."""
    response = api_client.get("/api/countries/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_textblock(api_client):
    """Тест для проверки доступности эндпоинта "/api/textblock/"."""
    response = api_client.get("/api/textblock/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_keywords(api_client):
    """Тест для проверки доступности эндпоинта "/api/keywords/"."""
    response = api_client.get("/api/keywords/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_transcriptions_save(api_client):
    """Тест для проверки доступности эндпоинта "/api/transcriptions_save/"."""
    response = api_client.get("/api/transcriptions_save/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_partial(api_client):
    """Тест для проверки доступности эндпоинта "/api/partial/"."""
    response = api_client.get("/api/partial/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"


@pytest.mark.django_db
def test_api_glossary(api_client):
    """Тест для проверки доступности эндпоинта "/api/glossary/"."""
    response = api_client.get("/api/glossary/")
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Ошибка {response.status_code} при открытиии запроса"
