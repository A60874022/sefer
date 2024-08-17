from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_create_api_textblock(api_client, textblock_payload) -> None:
    """Тест для проверки эндпоинта "/api/textblock/" при post запросе."""

    response_create = api_client.post(
        "/api/textblock/", data=textblock_payload, format="json"
    )
    textblock_id = response_create.data["id"]
    assert response_create.status_code == 201
    assert response_create.data["text"] == "Природа"

    response_read = api_client.get(f"/api/textblock/{textblock_id}/", format="json")
    assert response_read.status_code == HTTPStatus.OK
    assert response_read.data["text"] == "Природа"


@pytest.mark.django_db
def test_delete_api_textblock(api_client, create_textblock) -> None:
    """Тест для проверки эндпоинта "/api/textblock/" при delete запросе."""
    textblock_id = create_textblock.id
    response_delete = api_client.delete(
        f"/api/textblock/{textblock_id}/", format="json"
    )

    assert response_delete.status_code == HTTPStatus.NO_CONTENT
    response_read = api_client.get(f"/api/textblock/{textblock_id}/", format="json")
    assert response_read.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_api_textblock(api_client, create_textblock, textblock_payload) -> None:
    """Тест для проверки эндпоинта "/api/textblock/" при update запросе."""
    textblock_id = create_textblock.id

    response_update = api_client.patch(
        f"/api/textblock/{textblock_id}/", data=textblock_payload, format="json"
    )
    assert response_update.status_code == HTTPStatus.OK
    assert response_update.data["text"] == "Природа"

    response_update = api_client.patch(
        f"/api/cities/{textblock_id + 1}/", data=textblock_id, format="json"
    )
    assert response_update.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test__api_textblock(api_client, create_many_textblock, textblock_payload) -> None:
    """Тест для проверки эндпоинта "/api/textblock/?transcription=" при get запросе."""

    assert len(create_many_textblock) == 5

    transcription = create_many_textblock[0].transcription_id
    response_read = api_client.get(
        f"/api/textblock/?transcription={transcription}", format="json"
    )

    assert response_read.status_code == HTTPStatus.OK
    assert len(response_read.data) == 3
    assert response_read.data[2]["text"] == "1000"
