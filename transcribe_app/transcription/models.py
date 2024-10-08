import os

from django.db import models
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
from users.models import User


class Transcription(models.Model):
    """Класс транскрипции текста."""

    audio = models.FileField(
        "Аудио", upload_to="transcription/audio", blank=True, null=True
    )
    name = models.CharField("Название", max_length=60, blank=True)
    time_total = models.PositiveIntegerField("Длительность аудио", blank=True)
    code = models.CharField(
        "Шифр",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "Запись с таким шифром уже существует"},
    )
    transcription_status = models.CharField(
        "Статус расшифровки",
        max_length=20,
        choices=[
            ("not_sent", "-"),
            ("sent", "Отправлено"),
            ("received", "Готово"),
        ],
        default="not_sent",
    )
    transcription_date = models.DateTimeField(
        "Дата и время расшифровки", null=True, blank=True
    )
    last_updated = models.DateTimeField("Обновлено", auto_now=True)
    creator = models.ForeignKey(
        User,
        verbose_name="редактор",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Каталог записей"
        verbose_name_plural = "Каталоги записей"

    def __nonzero__(self):
        return bool(self.audio)


@receiver(models.signals.post_delete, sender=Transcription)
def auto_delete_media_file(sender, instance, *args, **kwargs):
    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)


class Country(models.Model):
    """Модель, представляющая Страны."""

    name = models.CharField(
        "Название (рус.)",
        max_length=100,
        unique=True,
        error_messages={"unique": "Страна с таким названием уже существует"},
    )
    name_en = models.CharField(
        "Название (англ.)",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "Страна с таким названием уже существует"},
    )
    category = models.CharField(
        "Категория",
        max_length=50,
        choices=[("modern", "Современное"), ("historical", "Историческое")],
        default="modern",
    )
    confirmed = models.CharField(
        "Подтверждено",
        choices=[
            ("Подтверждено", "Да"),
            ("Не подтверждено", "Нет"),
        ],
    )
    last_updated = models.DateTimeField("Обновлено", auto_now=True)
    creator = models.ForeignKey(
        User,
        verbose_name="редактор",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страну"
        verbose_name_plural = "Страны"


class City(models.Model):
    """Модель, представляющая Места."""

    name = models.CharField(
        "Название (рус)",
        max_length=100,
        unique=True,
        error_messages={"unique": "Место с таким названием уже существует"},
    )
    name_en = models.CharField(
        "Название (англ.)",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "Место с таким названием уже существует"},
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.DO_NOTHING,
        verbose_name="Страна",
        blank=True,
        null=True,
        related_name="cities",
    )
    last_updated = models.DateTimeField("Обновлено", auto_now=True)
    confirmed = models.CharField(
        "Подтверждено",
        choices=[
            ("Подтверждено", "Да"),
            ("Не подтверждено", "Нет"),
        ],
        default="Нет",
    )
    creator = models.ForeignKey(
        User,
        verbose_name="редактор",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Personalities(models.Model):
    """Модель, представляющая персоналии."""

    name = models.CharField("Имя (рус.)", max_length=100, unique=True)
    name_en = models.CharField(
        "Имя (англ.)", max_length=100, unique=True, null=True, blank=True
    )
    is_admin = models.BooleanField(default=False)
    last_updated = models.DateTimeField("Обновлено", auto_now=True)

    is_confirmed = models.CharField(
        "Подтверждено",
        choices=[
            ("Подтверждено", "Да"),
            ("Не подтверждено", "Нет"),
        ],
        default="Нет",
    )
    creator = models.ForeignKey(
        User,
        verbose_name="редактор",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персоналию"
        verbose_name_plural = "Персоналии"


class Keywords(MPTTModel):
    """Модель, представляющая ключевые слова."""

    name = models.CharField(
        "Название (рус.)",
        max_length=100,
        unique=True,
        error_messages={"unique": "Ключевое слово с таким названием уже существует"},
    )

    name_en = models.CharField(
        "Название (англ.)",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "Ключевое слово с таким названием уже существует"},
    )
    parent = TreeForeignKey(
        "Keywords",
        on_delete=models.CASCADE,
        verbose_name="Категория/Подкатегория",
        blank=True,
        null=True,
    )
    last_updated = models.DateTimeField("Обновлено", auto_now=True)
    creator = models.ForeignKey(
        User,
        verbose_name="редактор",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    class MPTTMeta:
        order_insertion_by = ["parent"]


class TextBlock(models.Model):
    """Модель текстовых блоков."""

    time_start = models.PositiveIntegerField("Начало текстового блока")
    time_end = models.PositiveIntegerField("Конец текстового блока")
    text = models.TextField("Текст")
    transcription = models.ForeignKey(
        Transcription, on_delete=models.CASCADE, related_name="text_blocks", blank=True
    )
    keywords = models.ManyToManyField(
        Keywords, blank=True, verbose_name="Ключевые слова"
    )
    personalities = models.ManyToManyField(
        Personalities, blank=True, verbose_name="Персоналии"
    )
    cities = models.ManyToManyField(City, blank=True, verbose_name="Города")
    countries = models.ManyToManyField(Country, blank=True, verbose_name="Страны")

    class Meta:
        verbose_name = "Текстовый_блок"
        verbose_name_plural = "Текстовые_блоки"

    def __str__(self) -> str:
        return f"Название транскрипции: {self.transcription.name}. "
