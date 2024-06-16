from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CityViewSet, CountryViewSet, GetGlossaryAPIView,
                    KeywordsViewSet, PersonalitiesViewSet, TextBlockViewSet,
                    TranscriptionShortList, TranscriptionViewSet, TranscriptionSaveViewSet)
from .yasg import urlpatterns as docs_url

router = DefaultRouter()
router.register(r"transcriptions",
                TranscriptionViewSet, basename="transcriptions")
router.register(r"personalities",
                PersonalitiesViewSet, basename="personalities")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"textblock", TextBlockViewSet, basename="textblock")
router.register(r"keywords", KeywordsViewSet, basename="keywords")
router.register(r"transcriptions_save", TranscriptionSaveViewSet, basename="transcriptions_save")

urlpatterns = [
    path("", include(router.urls)),
    path('transcription_list/', TranscriptionShortList.as_view(),
         name='transcription_list'),
    path(
        "transcriptions/<int:pk>/create_transcription",
        TranscriptionViewSet.as_view({"get": "create_transcription"}),
    ),
    path('glossary/', GetGlossaryAPIView.as_view(), name='glossary'),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]

urlpatterns += docs_url
