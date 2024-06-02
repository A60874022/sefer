from api.serializers import (CitySerializer, CountryGlossarySerializer,
                             CountrySerializer, KeywordsSerializer,
                             PersonalitiesSerializer, TextBlockSerializer,
                             TranscriptionSerializer,
                             TranscriptionShortSerializer)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock, Transcription)
from transcription.services import (create_bucket_url, create_transcription,
                                    delete_file_in_backet)

from .yasg import glossary_schema_dict


class KeywordsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KeywordsSerializer
    queryset = Keywords.objects.all()


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class PersonalitiesViewSet(ModelViewSet):
    serializer_class = PersonalitiesSerializer
    queryset = Personalities.objects.all()


class TextBlockViewSet(ModelViewSet):
    serializer_class = TextBlockSerializer
    queryset = TextBlock.objects.all()


class TranscriptionViewSet(ModelViewSet):
    """
    Вьюсет Транскрипции.
    Поддерживаемые методы по умолчанию `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    serializer_class = TranscriptionSerializer
    queryset = Transcription.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_file_in_backet(obj_id=instance.id)
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["retrieve"],
        url_name="create_transcription",
        url_path="create_transcription",
    )
    def create_transcription(self, request, pk=None):
        transcription = get_object_or_404(Transcription, pk=pk)
        transcription.audio_url = create_bucket_url(pk)
        text = create_transcription(pk)
        TextBlock.objects.bulk_create(
            [
                TextBlock(
                    minute=minute,
                    text=" ".join(chunk),
                    transcription=transcription
                )
                for minute, chunk in enumerate(text, start=1)
            ]
        )
        transcription.save()
        serializer = self.get_serializer(transcription)
        return Response(serializer.data)


class GetGlossaryAPIView(APIView):
    """
    Получение списка тэгов.
    """
    @swagger_auto_schema(responses=glossary_schema_dict)
    def get(self, request):
        glossary_data = {
            'keywords': KeywordsSerializer(Keywords.objects.all(), many=True).data,
            'countries': CountryGlossarySerializer(Country.objects.all(), many=True).data,
            'cities': CitySerializer(City.objects.all(), many=True).data,
            'personalities': PersonalitiesSerializer(Personalities.objects.all(), many=True).data
        }
        return Response(glossary_data)


class TranscriptionShortList(ListAPIView):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionShortSerializer
