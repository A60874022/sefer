from rest_framework.authentication import TokenAuthentication

from .models import CastomToken

class CastomTokenAuthentication(TokenAuthentication):
    """Переназначение модели токена."""

    model = CastomToken
