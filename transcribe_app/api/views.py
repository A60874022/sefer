from rest_framework.viewsets import ModelViewSet
from transcription.models import Trancription
from .serializers import TranscriptionSerializer


class TranscriptionViewSet(ModelViewSet):
    """Вьюсет Транскрипции."""
    serializer_class = TranscriptionSerializer
    queryset = Trancription.objects.all()
