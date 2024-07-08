from werkzeug.exceptions import Unauthorized
from collections.abc import Callable
from functools import wraps
from typing import Any
from hmac import compare_digest

from quart import request, has_request_context, has_websocket_context, current_app


def api_key_required(api_config_key: str = "API_KEY",) -> Callable:

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if has_request_context():
                api_key = request.headers.get("X-API-Key", "")
            elif has_websocket_context():
                api_key = websocket.headers.get("X-API-Key", "")
            else:
                raise RuntimeError("Not used in a valid request/websocket context")

            if (compare_digest(api_key, current_app.config[api_config_key])):
                return await current_app.ensure_async(func)(*args, **kwargs)
            else:
                raise Unauthorized()

        return wrapper

    return decorator