import base64
from django.db import transaction
from django.core.files.base import ContentFile
from django.db.models import ManyToManyField
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock, Transcription)
from transcription.services import create_transcription

class KeywordsSerializer(serializers.ModelSerializer):
    """Сериализатор для ключевых слов."""

    class Meta:
        model = Keywords
        fields = ("id", "name",)


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов."""

    class Meta:
        model = City
        fields = ("id", "name", "country")


class CountrySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран."""

    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class CountryGlossarySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран в глоссарии."""

    class Meta:
        model = Country
        fields = ("id", "name")


class PersonalitiesSerializer(serializers.ModelSerializer):
    """Сериализатор для персоналий."""

    class Meta:
        model = Personalities
        fields = ("id", "name",)


class TextBlockSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока."""
    
    class Meta:
        model = TextBlock
        fields = (
            "id", "minute", "text", "transcription",
            "keywords", "personalities", "cities", "countries"
        )


class TextBlockGetSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока при сохранении файла и ручной расшифровкой."""
   

    class Meta:
        model = TextBlock
        fields = (
            "id", "minute", "text"
        )


class Base64AudioField(serializers.FileField):
    """Функция для декодирования аудио файла из формата base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:audio"):
            format, audio_str = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(audio_str), name="temp." + ext)

        return super().to_internal_value(data)

class TranscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аудио для автоматической расшифровки."""

    audio = Base64AudioField()

    class Meta:
        model = Transcription
        fields = ("id", "name", "audio")
    @transaction.atomic
    def create(self, validated_data):
        """
        Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """
        transcription = Transcription.objects.create(**validated_data)
        last = Transcription.objects.filter(pk__gt=1).last()
        text = create_transcription(last.id)
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
        
        return validated_data


class TranscriptionShortSerializer(serializers.ModelSerializer):
    """Сериализатор для простого списка аудио."""
    class Meta:
        model = Transcription
        fields = ("id", "name")


class TranscriptionBaseSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аудио и при сохранении файла
      и ручной расшифровкой."""

    audio = Base64AudioField(required=False)
    text_blocks = TextBlockGetSerializer(
        many=True)

    class Meta:
        model = Transcription
        fields = ("id", "name", "audio", "text_blocks",)


    def create(self, validated_data):
        """
        Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """
        data_text_blocks = validated_data.pop("text_blocks")
        transcription = Transcription.objects.create(**validated_data)
        print(data_text_blocks )
        for block_data in data_text_blocks:
            TextBlock.objects.create(transcription=transcription,
                                                  **block_data)
        return transcription

    def update(self, instance, validated_data):
        """
        Обновление записи в том числе  и текстовых блоков.
        ВАЖНО: при обновлении и правке данных необходимо скопировать
        все текстовые блоки в патч запрос и только после этого редактировать,
        так как если будут переданы только старые данные то предыдущие
        будут утеряны.
        """
        if "text_blocks" in validated_data:
            data_text_blocks = validated_data.pop("text_blocks")
            instance.text_blocks.all().delete()  # Удаляем старые text_blocks
            for block_data in data_text_blocks:
                TextBlock.objects.create(transcription=instance,
                                                      **block_data)
        instance.save()
        return instance


class TranscriptionPartialSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки частичной автоматической расшифровки аудио."""

    audio = Base64AudioField()

    class Meta:
        model = Transcription
        fields = ("id", "name", "audio")


    #@transaction.atomic
    def create(self, instance, request, *args, **kwds):
        """
        Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """
        #partial = request.GET.get("partial")
        #transcription = Transcription.objects.create(**validated_data)
        print(instance, 124)
        return instance
        '''
        last = Transcription.objects.filter(pk__gt=1).last()
        text = create_transcription(last.id)
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
        
        return validated_data'''

    

