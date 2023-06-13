from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TranscriptionViewSet

router = DefaultRouter()
router.register(r"transcriptions", TranscriptionViewSet, basename="transcriptions")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "transcriptions/<int:pk>/get_transcription",
        TranscriptionViewSet.as_view({"get": "get_transcription"}),
    ),
]
