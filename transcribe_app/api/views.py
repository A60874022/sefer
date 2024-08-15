from api.serializers import (CitySerializer, CountryGlossarySerializer,
                             CountrySerializer, KeywordsSerializer,
                             PersonalitiesSerializer, TextBlockSerializer,
                             TranscriptionGetSerializer,
                             TranscriptionPartialSerializer,
                             TranscriptionSerializer)
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock, Transcription)
from transcription.services import (create_transcription,
                                    delete_file_in_backet,
                                    post_table_transcription)

from .yasg import glossary_schema_dict


class KeywordsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы со словами."""

    serializer_class = KeywordsSerializer
    queryset = Keywords.objects.all()


class CityViewSet(ModelViewSet):
    """Вьюсет для работы со городами."""

    serializer_class = CitySerializer
    queryset = City.objects.all()


class CountryViewSet(ModelViewSet):
    """Вьюсет для работы со странами."""

    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class PersonalitiesViewSet(ModelViewSet):
    """Вьюсет для работы с персоналиями."""

    serializer_class = PersonalitiesSerializer
    queryset = Personalities.objects.all()


class TextBlockViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с текстовыми блоками."""

    serializer_class = TextBlockSerializer
    queryset = TextBlock.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("transcription",)
    search_fields = ("transcription",)

    @transaction.atomic
    @action(
        detail=False,
        methods=["PATCH"],
        url_name="update_transcription",
        url_path="update_transcription",
    )
    def update_text_blocks(self, request):
        "Метод для обьединения текстовых блоков."
        try:
            textblock_id = [int(i) for i in request.GET.get("textblock_id").split(",")]
            text = request.data["text"]
        except:
            raise AssertionError("Ошибка при получении API")
        for i, id in enumerate(textblock_id):
            instance = TextBlock.objects.filter(id=id)
            if not instance:
                return Response(
                    {"error": "Этого текстового блока нет в списке"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if i == 0:
                TextBlock.objects.filter(id=id).update(text=text)
            else:
                instance.delete()
        return Response(status=status.HTTP_201_CREATED)


class TranscriptionViewSet(ModelViewSet):
    """Вьюсет для автоматической расшифровки всего обьема аудио."""

    serializer_class = TranscriptionSerializer
    queryset = Transcription.objects.all()

    def get_serializer_class(self):
        """Функция выбора класса - сериализатора в зависимости от метода."""
        if self.request.method == "GET":
            return TranscriptionGetSerializer
        return TranscriptionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_file_in_backet(obj_id=instance.id)
        return super().destroy(request, *args, **kwargs)


class GetGlossaryAPIView(APIView):
    """Получение списка тэгов."""

    @swagger_auto_schema(responses=glossary_schema_dict)
    def get(self, request):
        glossary_data = {
            "keywords": KeywordsSerializer(Keywords.objects.all(), many=True).data,
            "countries": CountryGlossarySerializer(
                Country.objects.all(), many=True
            ).data,
            "cities": CitySerializer(City.objects.all(), many=True).data,
            "personalities": PersonalitiesSerializer(
                Personalities.objects.all(), many=True
            ).data,
        }
        return Response(glossary_data)


class TranscriptionSaveViewSet(ModelViewSet):
    """Предназначен для сохранения, удаления,
    обновления файлов без расшифровки аудио."""

    queryset = Transcription.objects.all()
    serializer_class = TranscriptionPartialSerializer


class TranscriptionPartialViewSet(ModelViewSet):
    """Предназначен для частичной автоматической расшифровки аудио."""

    queryset = Transcription.objects.all()
    serializer_class = TranscriptionPartialSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """

        transcription = post_table_transcription(request, *args, **kwargs)
        partial = request.GET.get("partial")
        last = Transcription.objects.filter(pk__gt=1).last()
        text = create_transcription(last.id)
        TextBlock.objects.bulk_create(
            [
                TextBlock(
                    minute=minute, text=" ".join(chunk), transcription=transcription
                )
                for minute, chunk in enumerate(text, start=1)
                if str(minute) in partial
            ]
        )
        transcription.save()
        serializer = self.get_serializer(transcription)
        delete_file_in_backet(last.id)
        return Response(serializer.data)
