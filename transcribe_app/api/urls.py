from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CityViewSet,
    KeywordsViewSet,
    PersonalitiesViewSet,
    TextBlockViewSet,
    TranscriptionViewSet,
)
from .yasg import urlpatterns as docs_url

router = DefaultRouter()
router.register(r"transcriptions", TranscriptionViewSet, basename="transcriptions")
router.register(r"personalities", PersonalitiesViewSet, basename="personalities")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"textblock", TextBlockViewSet, basename="textblock")
router.register(r"keywords", KeywordsViewSet, basename="keywords")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "transcriptions/<int:pk>/create_transcription",
        TranscriptionViewSet.as_view({"get": "create_transcription"}),
    ),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]

urlpatterns += docs_url
