from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.timezone import now

from .models import (City, Country, Keywords, Personalities, TextBlock,
                     Transcription)


class TextBlockInline(admin.StackedInline):
    model = TextBlock
    extra = 1
    classes = ["collapse"]


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    """Класс для админпанели представления класса Transcription."""

    list_display = (
        "id",
        "name",
        "audio",
        "time_total",
        "code",
        "transcription_status",
        "transcription_date",
        "last_updated",
        "creator",
    )
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("transcription_status",)
    ordering = ("id", "name", "audio", "last_updated")
    inlines = [TextBlockInline]
    readonly_fields = ("id", "last_updated", "transcription_status", "creator",)

    def get_readonly_fields(self, request, obj=None):
        """
        Возвращает список неизменяемых полей
        в зависимости от условий или пользователя
        """
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """Метод для дополнительных действий при сохранении объекта"""
        if not obj.pk:
            pass
        super().save_model(request, obj, form, change)


@admin.register(City)
class CityAdmin(ModelAdmin):
    """Класс для админпанели представления класса City."""

    list_display = ("id", "name", "country", "last_updated", "confirmed", "creator")
    search_fields = ("id", "name", "confirmed")
    list_filter = ("country__cities", "confirmed")
    list_display_links = ("id", "name")
    readonly_fields = ("id", "last_updated")
    ordering = ("id", "name", "last_updated", "confirmed")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Только при создании нового объекта
            obj.creator = request.user
        obj.last_updated = now()
        super().save_model(request, obj, form, change)


@admin.register(Personalities)
class PersonalitiesAdmin(admin.ModelAdmin):
    """Класс для админпанели представления класса Personalities."""

    list_display = ("id", "name", "name_en", "is_confirmed", "last_updated", "creator")
    list_filter = ("is_confirmed",)
    search_fields = ("id", "name", "name_en")
    list_display_links = ("id", "name", "name_en")
    list_editable = ("is_confirmed",)
    readonly_fields = ("id", "last_updated")
    ordering = ("id", "name", "name_en", "last_updated")

    fieldsets = (
        (None, {"fields": ("name", "name_en", "is_confirmed")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("last_updated",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Только при создании нового объекта
            obj.creator = request.user
        obj.last_updated = now()
        super().save_model(request, obj, form, change)


@admin.register(Keywords)
class KeywordsAdmin(admin.ModelAdmin):
    """Класс для админпанели представления класса Keywords."""

    list_display = ("id", "name", "name_en", "parent", "last_updated")
    list_filter = (
        "name",
        "name_en",
        "last_updated",
    )
    list_display_links = ("id", "name", "name_en")
    search_fields = ("id", "name", "name_en", "parent")
    readonly_fields = (
        "id",
        "last_updated",
    )
    ordering = ("id", "name", "name_en", "last_updated")
    fieldsets = (
        (None, {"fields": ("name", "name_en", "parent")}),
        (
            "Дополнительная информация",
            {
                "fields": ("last_updated",),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    """Класс для админпанели представления класса Country."""

    list_display = (
        "id",
        "name",
        "name_en",
        "category",
        "last_updated",
        "confirmed",
    )
    list_filter = ("category", "confirmed")
    list_display_links = ("id", "name", "name_en")
    ordering = ("id", "name", "name_en", "confirmed")
    search_fields = ("id", "name", "name_en", "category", "confirmed")

    def make_confirmed(self, request, queryset):
        queryset.update(confirmed=True)

    fieldsets = ((None, {"fields": ("name", "name_en", "confirmed", "category")}),)
