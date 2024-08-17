import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock)

User = get_user_model()


@pytest.fixture
def creator():
    """Фикстура для создания пользователя в БД."""
    return User.objects.create_user(
        username="john1", email="js@js.com", password="js.sj"
    )


@pytest.fixture
def api_client(creator):
    """Фикстура для создания авторизованного клиента API."""
    user = User.objects.create_user(
        username="john", email="js@js.com", password="js.sj"
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def create_country():
    """Фикстура для создания записи о стране в БД."""
    return Country.objects.create(
        name="Россия", category="modern", confirmed="Подтверждено"
    )


@pytest.fixture
def create_keywords():
    """Фикстура для создания записи о слове в БД."""
    return Keywords.objects.create(name="Горы")


@pytest.fixture
def create_personalities(creator):
    """Фикстура для создания записи о персоналии в БД."""
    return Personalities.objects.create(name="Россия", creator_id=creator.id)


@pytest.fixture
def create_city(creator, create_country):
    """Фикстура для создания записи о городе в БД."""
    return City.objects.create(
        name="Пекин", country=create_country, creator_id=creator.id
    )


@pytest.fixture
def city_payload():
    """Фикстура для создания JSON для сущности город."""
    country = Country.objects.create(
        name="Россия", category="modern", confirmed="Подтверждено"
    )
    return {"name": "Москва", "country": country.id}


@pytest.fixture
def create_textblock(creator):
    """Фикстура для создания записи о текст-блоке в БД."""
    textblock_data = {
        'time_start': 1,
        'time_end': 2,
        'text': 'ракета',
    }
    return TextBlock.objects.create(**textblock_data)
