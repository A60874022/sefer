from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from transcription.models import TextBlock, Transcription
from transcription.services import create_bucket_url, create_transcription, \
                                   delete_file_in_backet

from .serializers import TranscriptionSerializer


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
        url_name="get_transcription",
        url_path="get_transcription",
    )
    def get_transcription(self, request, pk=None):
        transcription = get_object_or_404(Transcription, pk=pk)
        transcription.audio_url = create_bucket_url(pk)
        text = create_transcription(pk)
        TextBlock.objects.bulk_create(
            [
                TextBlock(minute=i,
                          text=" ".join(chunk),
                          transcription=transcription)
                for i, chunk in enumerate(text, start=1)
            ]
        )
        transcription.save()
        serializer = self.get_serializer(transcription)
        return Response(serializer.data)
