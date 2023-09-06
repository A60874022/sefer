from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from transcription.models import TextBlock, Transcription, Personalities, City
from django.core.exceptions import ObjectDoesNotExist


from transcription.services import (
    create_bucket_url,
    create_transcription,
    delete_file_in_backet,
)

from .serializers import (
    TranscriptionSerializer,
    TextBlockSerializer,
    PersonalitiesSerializer,
    CitySerializer,
    JoinTextBlocksSerializer,
)


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class PersonalitiesViewSet(ModelViewSet):
    serializer_class = PersonalitiesSerializer
    queryset = Personalities.objects.all()


class TextBlockViewSet(ModelViewSet):
    serializer_class = TextBlockSerializer
    queryset = TextBlock.objects.all()


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
                    minute=minute, text=" ".join(chunk), transcription=transcription
                )
                for minute, chunk in enumerate(text, start=1)
            ]
        )
        transcription.save()
        serializer = self.get_serializer(transcription)
        return Response(serializer.data)


@api_view(["POST"])
def join_transcription_text_blocks(request):
    serializer = JoinTextBlocksSerializer(data=request.data)
    if serializer.is_valid():
        trascription = get_object_or_404(
            Transcription, pk=serializer.data.get("transcription_id")
        )
        text_blocks = trascription.text_blocks.all()
        start_text_block = trascription.text_blocks.get(
            minute=serializer.data.get("start")
        )
        start_text_block.text = " ".join(
            [
                text_block.text
                for text_block in text_blocks[: serializer.data.get("end")]
            ]
        )
        start_text_block.save()
        for minute in range(
            serializer.data.get("start") + 1, serializer.data.get("end") + 1
        ):
            try:
                text_block = trascription.text_blocks.get(minute=minute)
                text_block.delete()
            except ObjectDoesNotExist:
                continue
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
