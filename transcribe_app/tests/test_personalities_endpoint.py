from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_api_personalities(api_client) -> None:
    """Тест для проверки эндпоинта "/api/personalities/" при post запросе."""
    creator = User.objects.create_user(username='john1', email='js@js.com', password='js.sj')
    payload = {'name': 'Россия', 'creator_id': creator.id
               }
    response_create = api_client.post("/api/personalities/", data=payload, format="json")
    personalities_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["name"] == 'Россия'

    response_read = api_client.get(f"/api/personalities/{personalities_id}/", format="json")
    assert response_read.status_code == HTTPStatus.OK
    assert response_read.data["name"] == "Россия"


@pytest.mark.django_db
def test_delete_api_personalities(api_client, create_personalities) -> None:
    """Тест для проверки эндпоинта "/api/personalities/" при delete запросе."""
    personalities_id = create_personalities.id
    response_delete = api_client.delete(f"/api/personalities/{personalities_id}/", format="json")
    assert response_delete.status_code == HTTPStatus.NO_CONTENT
    response_read = api_client.get(f"/api/personalities/{personalities_id}/", format="json")
    assert response_read.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_api_personalities(api_client, create_personalities) -> None:
    """Тест для проверки эндпоинта "/api/personalities/" при delete запросе."""

    payload = {'name': 'Китай',
               }
    personalities_id = create_personalities.id
    response_update = api_client.patch(
        f"/api/personalities/{personalities_id}/", data=payload, format="json")

    assert response_update.status_code == HTTPStatus.OK
    assert response_update.data["name"] == "Китай"

    response_update = api_client.patch(
        f"/api/personalities/{personalities_id + 1}/", data=payload, format="json")
    assert response_update.status_code == HTTPStatus.NOT_FOUND
