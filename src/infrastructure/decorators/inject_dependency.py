import inspect
from functools import wraps
from typing import Any, Callable

from injector import Injector


def inject_dependency(default_injector: Injector):
    """
    If the function has a parameter named 'injector', we pass it.
    Otherwise, we don't.
    Then, for each other parameter that isn't provided, we resolve from the injector.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        sig = inspect.signature(func)
        param_names = set(sig.parameters.keys())

        @wraps(func)
        def wrapper(*args, **kwargs):
            # If the function has a param called 'injector', and
            # the caller didn't provide it, default to the decorator's injector.
            if "injector" in param_names and "injector" not in kwargs:
                kwargs["injector"] = default_injector

            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()

            # For each param in the function signature
            for param_name, param in sig.parameters.items():
                # If the caller didn't provide it...
                if param_name not in bound_args.arguments:
                    annotated_type = param.annotation
                    # Must have a type hint
                    if annotated_type != inspect.Parameter.empty:
                        # We'll pick whichever injector is in the final bound_args
                        # If 'injector' doesn't exist in the final bound_args, fall back to default
                        used_injector = bound_args.arguments.get("injector", default_injector)
                        dependency = used_injector.get(annotated_type)
                        bound_args.arguments[param_name] = dependency

            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
