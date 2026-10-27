from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .external_api import ExternalAPIError, get_external_posts


@extend_schema(
    summary="Отримати дані із зовнішнього REST API",
    description=(
        "Отримує список публікацій із JSONPlaceholder. "
        "Підтримує тайм-аут, обробку мережевих помилок "
        "та кешування результатів на 5 хвилин."
    ),
    responses={
        200: inline_serializer(
            name="ExternalPostsResponse",
            fields={
                "source": serializers.CharField(),
                "data": serializers.ListField(child=serializers.DictField()),
            },
        ),
        503: inline_serializer(
            name="ExternalAPIErrorResponse",
            fields={
                "error": serializers.CharField(),
            },
        ),
    },
    tags=["Зовнішній REST API"],
)
@api_view(["GET"])
def external_posts(request):
    try:
        result = get_external_posts()

    except ExternalAPIError as exc:
        return Response(
            {"error": str(exc)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response(
        result,
        status=status.HTTP_200_OK,
    )
