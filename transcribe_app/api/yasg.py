from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Transcription API",
        default_version="v1",
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "swagger(?P<format>/.json|/.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

glossary_schema_dict = {
    200: openapi.Response(
        description="",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type="object",
                    properties={
                        "keywords": openapi.Schema(
                            type="array",
                            items=openapi.Schema(
                                type="object",
                                properties={
                                    "id": openapi.Schema(type="integer"),
                                    "name": openapi.Schema(type="string"),
                                },
                            ),
                        ),
                        "countries": openapi.Schema(
                            type="array",
                            items=openapi.Schema(
                                type="object",
                                properties={
                                    "id": openapi.Schema(type="integer"),
                                    "name": openapi.Schema(type="string"),
                                },
                            ),
                        ),
                        "cities": openapi.Schema(
                            type="array",
                            items=openapi.Schema(
                                type="object",
                                properties={
                                    "id": openapi.Schema(type="integer"),
                                    "name": openapi.Schema(type="string"),
                                },
                            ),
                        ),
                        "personalities": openapi.Schema(
                            type="array",
                            items=openapi.Schema(
                                type="object",
                                properties={
                                    "id": openapi.Schema(type="integer"),
                                    "name": openapi.Schema(type="string"),
                                },
                            ),
                        ),
                    },
                )
            }
        },
    )
}
