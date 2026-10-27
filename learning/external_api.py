import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class ExternalAPIError(Exception):
    """Помилка отримання даних із зовнішнього API."""


def get_external_posts():
    cache_key = "external_api_posts"

    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return {
            "source": "cache",
            "data": cached_data,
        }

    url = f"{settings.EXTERNAL_API_URL.rstrip('/')}/posts"

    try:
        response = requests.get(
            url,
            timeout=settings.EXTERNAL_API_TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise ExternalAPIError("Зовнішній API повернув некоректний формат даних.")

    except requests.Timeout as exc:
        logger.warning("Тайм-аут зовнішнього API: %s", exc)
        raise ExternalAPIError("Зовнішній сервіс не відповів вчасно.") from exc

    except requests.RequestException as exc:
        logger.warning("Помилка зовнішнього API: %s", exc)
        raise ExternalAPIError(
            "Не вдалося отримати дані із зовнішнього сервісу."
        ) from exc

    except ValueError as exc:
        logger.warning("Некоректний JSON зовнішнього API: %s", exc)
        raise ExternalAPIError("Зовнішній сервіс повернув некоректний JSON.") from exc

    cache.set(
        cache_key,
        data,
        timeout=settings.EXTERNAL_API_CACHE_TIMEOUT,
    )

    return {
        "source": "external_api",
        "data": data,
    }
