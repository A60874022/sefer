from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CityViewSet, CountryViewSet, EmptyTextBlockViewSet,
                    GetGlossaryAPIView, KeywordsViewSet, PersonalitiesViewSet,
                    TextBlockViewSet, TranscriptionPartialViewSet,
                    TranscriptionSaveViewSet, TranscriptionViewSet)
from .yasg import urlpatterns as docs_url

router = DefaultRouter()
router.register(r"transcriptions", TranscriptionViewSet, basename="transcriptions")
router.register(r"personalities", PersonalitiesViewSet, basename="personalities")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"textblock", TextBlockViewSet, basename="textblock")
router.register(r"keywords", KeywordsViewSet, basename="keywords")
router.register(
    r"transcriptions_save", TranscriptionSaveViewSet, basename="transcriptions_save"
)
router.register(r"partial", TranscriptionPartialViewSet, basename="partial")
router.register(r"empty_block", EmptyTextBlockViewSet, basename="empty_text_block")

urlpatterns = [
    path("", include(router.urls)),
    path("glossary/", GetGlossaryAPIView.as_view(), name="glossary"),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]

urlpatterns += docs_url
