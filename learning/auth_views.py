from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Це ім'я користувача вже зайняте.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


@extend_schema(
    request=RegisterSerializer,
    responses={
        201: inline_serializer(
            name="RegisterResponse",
            fields={
                "message": serializers.CharField(),
                "id": serializers.IntegerField(),
                "username": serializers.CharField(),
            },
        )
    },
    auth=[],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
        {
            "message": "Користувача успішно зареєстровано.",
            "id": user.pk,
            "username": user.username,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    request=inline_serializer(
        name="LogoutRequest",
        fields={
            "refresh": serializers.CharField(),
        },
    ),
    responses={
        200: inline_serializer(
            name="LogoutResponse",
            fields={"message": serializers.CharField()},
        )
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(
            {"detail": "Необхідно передати refresh-токен."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        token = RefreshToken(refresh_token)

        if str(token["user_id"]) != str(request.user.pk):
            return Response(
                {"detail": "Токен не належить поточному користувачу."},
                status=status.HTTP_403_FORBIDDEN,
            )

        token.blacklist()
    except TokenError:
        return Response(
            {"detail": "Недійсний або відкликаний refresh-токен."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"message": "Вихід виконано. Refresh-токен відкликано."},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    responses={
        200: inline_serializer(
            name="CurrentUserResponse",
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField(),
                "email": serializers.EmailField(),
            },
        )
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(
        {
            "id": request.user.pk,
            "username": request.user.username,
            "email": request.user.email,
        }
    )
