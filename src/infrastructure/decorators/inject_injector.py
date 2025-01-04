from functools import wraps
from typing import Any, Callable

from injector import Injector


def inject_injector(injector: Injector):
    """A decorator that provides the given injector to the function as a parameter."""

    def decorator(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Only set 'injector' if it's not already present
            kwargs.setdefault("injector", injector)

            return func(*args, **kwargs)

        return wrapper

    return decorator
