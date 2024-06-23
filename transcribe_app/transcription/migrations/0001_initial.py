# Generated by Django 4.2.1 on 2024-06-23 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Место"),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "confirmed",
                    models.BooleanField(default=True, verbose_name="Подтверждено?"),
                ),
            ],
            options={
                "verbose_name": "Место",
                "verbose_name_plural": "Места",
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Страна"
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "confirmed",
                    models.BooleanField(default=True, verbose_name="Подтверждено?"),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("modern", "Современное"),
                            ("historical", "Историческое"),
                        ],
                        default="modern",
                        max_length=50,
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
            },
        ),
        migrations.CreateModel(
            name="Keywords",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        verbose_name="Ключевое слово (рус.)",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Ключевое слово (англ.)",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="transcription.keywords",
                        verbose_name="родитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ключевое слово",
                "verbose_name_plural": "Ключевые слова",
            },
        ),
        migrations.CreateModel(
            name="Personalities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Персоналия"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Имя (англ.)",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "is_confirmed",
                    models.BooleanField(default=True, verbose_name="Подтверждено"),
                ),
            ],
            options={
                "verbose_name": "Персоналия",
                "verbose_name_plural": "Персоналии",
            },
        ),
        migrations.CreateModel(
            name="Transcription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "audio",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="transcription/audio",
                        verbose_name="Аудио",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=60, verbose_name="Название"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Шифр",
                    ),
                ),
                (
                    "transcription_status",
                    models.CharField(
                        choices=[
                            ("not_sent", "Не отправлено"),
                            ("sent", "Отправлено"),
                            ("received", "Готово"),
                        ],
                        default="not_sent",
                        max_length=20,
                        verbose_name="Статус расшифровки",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
            ],
            options={
                "verbose_name": "Транскрипция",
                "verbose_name_plural": "Транскрипции",
            },
        ),
        migrations.CreateModel(
            name="TextBlock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("minute", models.PositiveIntegerField(verbose_name="Минута")),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "cities",
                    models.ManyToManyField(
                        blank=True, to="transcription.city", verbose_name="Города"
                    ),
                ),
                (
                    "countries",
                    models.ManyToManyField(
                        blank=True, to="transcription.country", verbose_name="Страны"
                    ),
                ),
                (
                    "keywords",
                    models.ManyToManyField(
                        blank=True,
                        to="transcription.keywords",
                        verbose_name="Ключевые слова",
                    ),
                ),
                (
                    "personalities",
                    models.ManyToManyField(
                        blank=True,
                        to="transcription.personalities",
                        verbose_name="Персоналии",
                    ),
                ),
                (
                    "transcription",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="text_blocks",
                        to="transcription.transcription",
                    ),
                ),
            ],
            options={
                "verbose_name": "Текстовый_блок",
                "verbose_name_plural": "Текстовые_блоки",
            },
        ),
        migrations.AddField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="cities",
                to="transcription.country",
                verbose_name="Страна",
            ),
        ),
        migrations.AddConstraint(
            model_name="textblock",
            constraint=models.UniqueConstraint(
                fields=("minute", "text", "transcription"),
                name="uniq_transcriptions_text_block",
            ),
        ),
    ]
