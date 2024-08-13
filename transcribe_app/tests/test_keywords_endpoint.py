from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_create_api_keywords(api_client, create_keywords) -> None:
    """Тест для проверки эндпоинта "/api/keywords/" при get запросе."""

    keywords_id = create_keywords.id
    response_read = api_client.get(f"/api/keywords/{keywords_id}/", format="json")
    assert response_read.status_code == HTTPStatus.OK
