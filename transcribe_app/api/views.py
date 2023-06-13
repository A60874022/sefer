from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from transcription.models import Transcription
from transcription.services import create_bucket_url, create_transcription

from .serializers import TranscriptionSerializer


class TranscriptionViewSet(ModelViewSet):
    """Вьюсет Транскрипции."""

    serializer_class = TranscriptionSerializer
    queryset = Transcription.objects.all()

    @action(
        detail=False,
        methods=["retrieve"],
        url_name="get_transcription",
        url_path="get_transcription",
    )
    def get_transcription(self, request, pk=None):
        transcription = get_object_or_404(Transcription, pk=pk)
        transcription.audio_url = create_bucket_url(pk)
        transcription.text = create_transcription(pk)
        transcription.save()
        response = Response(
            {
                "audio_url": f"{transcription.audio_url}",
                "text": f"{transcription.text}",
            },
        )
        return response
