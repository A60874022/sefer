from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_create_api_cities(api_client, сity_payload) -> None:
    """Тест для проверки эндпоинта "/api/cities/" при post запросе."""

    response_create = api_client.post("/api/cities/", data=сity_payload, format="json")
    cities_id = response_create.data["id"]
    assert response_create.status_code == HTTPStatus.CREATED
    assert response_create.data["name"] == сity_payload["name"]

    response_read = api_client.get(f"/api/cities/{cities_id}/", format="json")
    assert response_read.status_code == HTTPStatus.OK
    assert response_read.data["name"] == "Москва"


@pytest.mark.django_db
def test_delete_api_cities(api_client, create_city) -> None:
    """Тест для проверки эндпоинта "/api/cities/" при delete запросе."""
    cities_id = create_city.id
    response_delete = api_client.delete(f"/api/cities/{cities_id}/", format="json")
    assert response_delete.status_code == HTTPStatus.NO_CONTENT
    response_read = api_client.get(f"/api/cities/{cities_id}/", format="json")
    assert response_read.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_api_cities(api_client, create_city, сity_payload) -> None:
    """Тест для проверки эндпоинта "/api/cities/" при update запросе."""
    cities_id = create_city.id

    response_update = api_client.patch(
        f"/api/cities/{cities_id}/", data=сity_payload, format="json"
    )
    assert response_update.status_code == HTTPStatus.OK
    assert response_update.data["name"] == "Москва"

    response_update = api_client.patch(
        f"/api/cities/{cities_id + 1}/", data=сity_payload, format="json"
    )
    assert response_update.status_code == HTTPStatus.NOT_FOUND
