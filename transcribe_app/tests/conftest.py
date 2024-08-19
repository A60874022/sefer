import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock, Transcription)

User = get_user_model()


@pytest.fixture
def creator():
    return User.objects.create_user(
        username="john1", email="js@js.com", password="js.sj"
    )


@pytest.fixture
def api_client():
    """Фикстура для создания записи о авторизованном пользователи в БД."""
    user = User.objects.create_user(
        username="john", email="js@js.com", password="js.sj"
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def create_countries():
    """Фикстура для создания записи о стране в БД."""
    return Country.objects.create(
        name="Россия", category="modern", confirmed="Подтверждено"
    )


@pytest.fixture
def countries_payload():
    """Фикстура для создания json для сущности страна."""
    return {"name": "Россия", "category": "modern", "confirmed": "Подтверждено"}


@pytest.fixture
def create_keywords():
    """Фикстура для создания записи о слове в БД."""
    return Keywords.objects.create(name="Горы")


@pytest.fixture
def create_personalities(creator):
    """Фикстура для создания записи о персаналии в БД ."""
    return Personalities.objects.create(name="Россия", creator_id=creator.id)


@pytest.fixture
def personalities_payload(creator):
    """Фикстура для создания json для сущности персаналии."""
    return {"name": "Россия", "creator_id": creator.id}


@pytest.fixture
def create_city(creator, create_countries):
    """Фикстура для создания записи о городе в БД."""
    return City.objects.create(
        name="Пекин", country_id=create_countries.id, creator_id=creator.id
    )


@pytest.fixture
def сity_payload(create_countries):
    """Фикстура для создания json для сущности город."""
    return {"name": "Москва", "country": create_countries.id}


@pytest.fixture
def create_transcription_2(creator):
    """Фикстура для создания записи о аудиозаписи в БД."""
    return Transcription.objects.create(
        name="Горы",
        code="modern",
        transcription_status="not_sent",
        creator_id=creator.id,
    )


@pytest.fixture
def create_transcription(creator):
    """Фикстура для создания записи о аудиозаписи в БД."""
    return Transcription.objects.create(
        name="Россия",
        code="озера",
        transcription_status="not_sent",
        creator_id=creator.id,
    )


@pytest.fixture
def create_textblock(creator, create_transcription):
    """Фикстура для создания записи о текст-блоке в БД."""
    textblock_data = {
        "time_start": 1,
        "time_end": 2,
        "text": "ракета",
        "transcription_id": create_transcription.id,
    }
    return TextBlock.objects.create(**textblock_data)


@pytest.fixture
def textblock_payload(creator, create_transcription):
    """Фикстура для создания json для сущности текстовый блок."""
    return {
        "time_start": 1,
        "time_end": 2,
        "text": "Природа",
        "transcription": create_transcription.id,
    }


@pytest.fixture
def create_many_textblock(creator, create_transcription, create_transcription_2):
    """Фикстура для создания записи в текст-блоке в БД."""
    textblock_data = [
        {
            "time_start": 1,
            "time_end": 2,
            "text": "1",
            "transcription_id": create_transcription.id,
        },
        {
            "time_start": 3,
            "time_end": 4,
            "text": "10",
            "transcription_id": create_transcription.id,
        },
        {
            "time_start": 2,
            "time_end": 4,
            "text": "100",
            "transcription_id": create_transcription_2.id,
        },
        {
            "time_start": 5,
            "time_end": 7,
            "text": "1000",
            "transcription_id": create_transcription.id,
        },
        {
            "time_start": 6,
            "time_end": 8,
            "text": "10000",
            "transcription_id": create_transcription_2.id,
        },
    ]
    new_textblock_objs = [TextBlock(**textblock) for textblock in textblock_data]
    return TextBlock.objects.bulk_create(new_textblock_objs)


@pytest.fixture
def textblock_payload_update(creator, create_transcription):
    """Фикстура для создания json для сущности текстовый блок."""
    return [
        {
            "time_start": 1,
            "time_end": 2,
            "text": "тестовые данные 1",
            "transcription": create_transcription.id,
        },
        {
            "time_start": 3,
            "time_end": 4,
            "text": "тестовые данные 2",
            "transcription": create_transcription.id,
        },
    ]
