from rest_framework.viewsets import ModelViewSet
from transcription.models import Transcription
from .serializers import TranscriptionSerializer


class TranscriptionViewSet(ModelViewSet):
    """Вьюсет Транскрипции."""
    serializer_class = TranscriptionSerializer
    queryset = Transcription.objects.all()
