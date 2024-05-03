from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import (City, Country, Keywords, Personalities, TextBlock,
                     Transcription)


class TextBlockInline(admin.StackedInline):
    model = TextBlock


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    inlines = [TextBlockInline]


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ("name", "country", "is_admin")
    list_filter = ("country",)


@admin.register(Personalities)
class PersonalitiesAdmin(ModelAdmin):
    list_display = ("name", "is_admin")
    list_filter = ("name",)


@admin.register(Keywords)
class KeywordsAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ("name", "is_admin")
    search_fields = ("name",)
