from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    status_code = response.status_code

    titles = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
    }

    if status_code == 400:
        error_type = "validation_error"
        detail = "Передані дані містять помилки."

    elif status_code == 404:
        error_type = "not_found"
        detail = "Запитаний ресурс не знайдено."

    else:
        error_type = "api_error"
        detail = "Під час виконання запиту виникла помилка."

    original_errors = response.data

    response.data = {
        "type": error_type,
        "title": titles.get(
            status_code,
            "API Error",
        ),
        "status": status_code,
        "detail": detail,
        "errors": original_errors,
    }

    return response