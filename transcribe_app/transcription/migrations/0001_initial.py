# Generated by Django 4.2.1 on 2024-09-08 05:54

from django.db import migrations, models


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
                    models.CharField(
                        error_messages={
                            "unique": "Место с таким названием уже существует"
                        },
                        max_length=100,
                        unique=True,
                        verbose_name="Название (рус)",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Место с таким названием уже существует"
                        },
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Название (англ.)",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "confirmed",
                    models.CharField(
                        choices=[("Подтверждено", "Да"), ("Не подтверждено", "Нет")],
                        default="Нет",
                        verbose_name="Подтверждено",
                    ),
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
                        error_messages={
                            "unique": "Страна с таким названием уже существует"
                        },
                        max_length=100,
                        unique=True,
                        verbose_name="Название (рус.)",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Страна с таким названием уже существует"
                        },
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Название (англ.)",
                    ),
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
                (
                    "confirmed",
                    models.CharField(
                        choices=[("Подтверждено", "Да"), ("Не подтверждено", "Нет")],
                        verbose_name="Подтверждено",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
            ],
            options={
                "verbose_name": "Страну",
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
                        error_messages={
                            "unique": "Ключевое слово с таким названием уже существует"
                        },
                        max_length=100,
                        unique=True,
                        verbose_name="Название (рус.)",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Ключевое слово с таким названием уже существует"
                        },
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="Название (англ.)",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
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
                        max_length=100, unique=True, verbose_name="Имя (рус.)"
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
                    models.CharField(
                        choices=[("Подтверждено", "Да"), ("Не подтверждено", "Нет")],
                        default="Нет",
                        verbose_name="Подтверждено",
                    ),
                ),
            ],
            options={
                "verbose_name": "Персоналию",
                "verbose_name_plural": "Персоналии",
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
                (
                    "time_start",
                    models.PositiveIntegerField(verbose_name="Начало текстового блока"),
                ),
                (
                    "time_end",
                    models.PositiveIntegerField(verbose_name="Конец текстового блока"),
                ),
                ("text", models.TextField(verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Текстовый_блок",
                "verbose_name_plural": "Текстовые_блоки",
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
                    "time_total",
                    models.PositiveIntegerField(
                        blank=True, verbose_name="Длительность аудио"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Запись с таким шифром уже существует"
                        },
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
                            ("not_sent", "-"),
                            ("sent", "Отправлено"),
                            ("received", "Готово"),
                        ],
                        default="not_sent",
                        max_length=20,
                        verbose_name="Статус расшифровки",
                    ),
                ),
                (
                    "transcription_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата и время расшифровки"
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
            ],
            options={
                "verbose_name": "Каталог записей",
                "verbose_name_plural": "Каталоги записей",
            },
        ),
    ]
