import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from transcription.models import Country, Keywords, Personalities

User = get_user_model()


@pytest.fixture
def api_client():
    """Фикстура для создания авторизованного пользователя."""
    user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def create_countries():
    country = Country.objects.create(
        name='Россия', category="modern", confirmed="Подтверждено")
    return country


@pytest.fixture
def create_keywords():
    keywords = Keywords.objects.create(
        name='Горы')
    return keywords


@pytest.fixture
def create_personalities():
    creator = User.objects.create_user(username='john1', email='js@js.com', password='js.sj')
    personalities = Personalities.objects.create(
        name='Россия', creator_id=creator.id
    )
    return personalities
