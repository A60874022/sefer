from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_create_api_countries(api_client) -> None:
    """Тест для проверки эндпоинта "/api/countries/" при post запросе."""
    payload = {"name": "Россия", "category": "modern", "сategory": "Подтверждено"}

    response_create = api_client.post("/api/countries/", data=payload, format="json")
    countries_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == payload["name"]

    response_read = api_client.get(f"/api/countries/{countries_id}/", format="json")
    assert response_read.status_code == HTTPStatus.OK
    assert response_read.data["name"] == "Россия"


@pytest.mark.django_db
def test_delete_api_countries(api_client, create_countries) -> None:
    """Тест для проверки эндпоинта "/api/countries/" при delete запросе."""
    countries_id = create_countries.id
    response_delete = api_client.delete(
        f"/api/countries/{countries_id}/", format="json"
    )
    assert response_delete.status_code == HTTPStatus.NO_CONTENT
    response_read = api_client.get(f"/api/countries/{countries_id}/", format="json")
    assert response_read.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_api_countries(api_client, create_countries) -> None:
    """Тест для проверки эндпоинта "/api/countries/" при delete запросе."""
    countries_id = create_countries.id
    payload = {"name": "Китай", "category": "modern", "confirmed": "Подтверждено"}

    response_update = api_client.patch(
        f"/api/countries/{countries_id}/", data=payload, format="json"
    )

    assert response_update.status_code == HTTPStatus.OK
    assert response_update.data["name"] == "Китай"

    response_update = api_client.patch(
        f"/api/countries/{countries_id + 1}/", data=payload, format="json"
    )
    assert response_update.status_code == HTTPStatus.NOT_FOUND
