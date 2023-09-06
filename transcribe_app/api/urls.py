from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TranscriptionViewSet,
    TextBlockViewSet,
    PersonalitiesViewSet,
    CityViewSet,
    join_transcription_text_blocks,
)
from .yasg import urlpatterns as docs_url

router = DefaultRouter()
router.register(r"transcriptions", TranscriptionViewSet, basename="transcriptions")
router.register(r"personalities", PersonalitiesViewSet, basename="personalities")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"textblock", TextBlockViewSet, basename="textblock")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "transcriptions/<int:pk>/create_transcription",
        TranscriptionViewSet.as_view({"get": "create_transcription"}),
    ),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "join_trascription_text_blocks/",
        join_transcription_text_blocks,
        name="join_trenscription_text_blocks",
    ),
]

urlpatterns += docs_url
