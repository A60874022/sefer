from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.timezone import now

from .models import (City, Country, Keywords, Personalities, TextBlock,
                     Transcription)


class TextBlockInline(admin.StackedInline):
    model = TextBlock
    extra = 1


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'audio', "audio_duration", 'code',
        'transcription_status', "transcription_date", 'last_updated', "creator")
    search_fields = ('id', 'name')
    list_filter = ('transcription_status',)
    ordering = ('id', 'name', 'audio', 'last_updated')
    inlines = [TextBlockInline]
    readonly_fields = ('id', 'last_updated')

    def audio_duration(self, obj):
        """
        Возвращает длительность аудиофайла в формате минуты:секунды.
        """
        pass  # нужно уточнить возможное решение

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
    list_display = ("id", "name", "country", "last_updated", "confirmed", 'creator')
    search_fields = ('id', "name", "confirmed")
    list_filter = ("country__cities", "confirmed")

    readonly_fields = ('id', 'last_updated')
    ordering = ('id', 'name', 'last_updated', "confirmed")

    '''def make_confirmed(self, request, queryset):
        queryset.update(confirmed=True)

    make_confirmed.short_description = "Отметьте выбранные места как подтвержденные"  # noqa'''

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Только при создании нового объекта
            obj.creator = request.user
        obj.last_updated = now()
        super().save_model(request, obj, form, change)


@admin.register(Personalities)
class PersonalitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_en', 'is_confirmed', 'last_updated', 'creator')
    list_filter = ('is_confirmed',)
    search_fields = ('id', 'name', 'name_en')
    list_display_links = ('id', 'name', 'name_en')
    list_editable = ('is_confirmed',)
    readonly_fields = ('id', 'last_updated')
    ordering = ('id', 'name', 'name_en', 'last_updated')

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
    list_display = ('id', 'name', 'name_en', 'parent', 'last_updated')
    list_filter = ('name', 'name_en', 'last_updated',)
    search_fields = ("id", 'name', 'name_en', 'parent')
    readonly_fields = ('id', 'last_updated')
    ordering = ('id', 'name', 'name_en', 'last_updated')
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
    list_display = ("id", "name", "name_en", "category", "last_updated", "confirmed", )
    list_filter = ("category", "confirmed")
    ordering = ('id', 'name', 'name_en', "confirmed")
    search_fields = ("id", "name", "name_en", "category", "confirmed")

    def make_confirmed(self, request, queryset):
        queryset.update(confirmed=True)

    fieldsets = (
        (None, {"fields": ("name", "name_en", "confirmed", "category")}),
    )


@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'minute', 'text', "transcription")
