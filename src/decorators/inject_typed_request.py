import functools
import inspect
from typing import Any, Callable

from flask import Request


def inject_typed_request():
    """
    A custom decorator that:
      1) Expects the first argument at runtime to be a Flask `Request`.
      2) Inspects the decorated function’s first parameter, ensures it has a type annotation
         (e.g., `GreetingRequest`) that provides a `.from_dict(...)` constructor or similar.
      3) Deserializes the HTTP request JSON into that typed model, replacing the raw `Request`
         argument with the constructed model for the decorated function.

    Usage:
        from flask import Request

        class GreetingRequest:
            first_name: str
            last_name: str

            @classmethod
            def from_dict(cls, data: dict) -> "GreetingRequest":
                # The typed decorator will call this to parse incoming JSON
                return cls.model_validate(data)

        @inject_typed_request
        def say_hello(req: GreetingRequest):
            # 'req' is now a strongly typed GreetingRequest,
            # populated from the HTTP request JSON.
            return {"message": f"Hello, {req.first_name} {req.last_name}"}

        # The framework (e.g., Functions Framework for Python) calls:
        # say_hello(flask_request)
        # -> the decorator deserializes the JSON into GreetingRequest
        # -> calls say_hello(req=GreetingRequest(...))
        # -> returns a dict or your specified return type.

    Notes:
      - If your typed model uses a different method than `.from_dict(...)`
        (e.g., Pydantic’s `.parse_obj(...)`), adjust the code accordingly.
      - If the returned object has a `.to_dict()` method, the decorator converts
        it to a dict so Flask can automatically handle the JSON response.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # 1. Reflect on the original function's signature
            sig = inspect.signature(func)
            parameters = list(sig.parameters.values())
            if not parameters:
                raise TypeError(f"Function {func.__name__} has no parameters. " "Cannot infer typed request parameter.")

            # 2. The first parameter must have a type annotation, e.g. GreetingRequest
            first_param = parameters[0]
            annotated_type = first_param.annotation
            if annotated_type is inspect._empty:
                raise TypeError(
                    f"Function {func.__name__}'s first parameter '{first_param.name}' "
                    "is not annotated with a type. Please provide a type annotation."
                )

            # 3. We expect the first *runtime* argument to be a Flask Request
            if not args:
                raise ValueError("No arguments provided at runtime (expected a Flask Request).")

            maybe_request = args[0]
            if not isinstance(maybe_request, Request):
                raise TypeError(f"Expected the first argument to be a Flask Request, but got {type(maybe_request)}")

            flask_request: Request = maybe_request

            # 4. Deserialize JSON body from the Flask Request
            json_data = flask_request.get_json(silent=True) or {}

            # 4.1. Query params as a dict
            query_data = dict(flask_request.args)  # e.g. {"foo":"123","bar":"xyz"}

            # 4.2. Headers (convert keys to a consistent pattern, e.g. lowercase + underscores)
            #    or keep them as-is if you prefer.
            header_data = {}
            # TODO: We can enable below code block if it is needed.
            # for k, v in flask_request.headers.items():
            #     # Example: "X-Custom-Token" -> "x_custom_token"
            #     # Convert header name to lowercase and underscores:
            #     # e.g. "X-Custom-Token" -> "x_custom_token"
            #     normalized_key = k.lower().replace("-", "_")

            #     # Only add headers that start with "x-" (or whatever logic you need)
            #     if normalized_key.startswith("x_"):
            #         header_data[normalized_key] = v

            # 4.3. Merge them (order can matter if you want body to override query, etc.)
            # For example, if query_data should override JSON, do: {**json_data, **query_data}
            merged_data = {**json_data, **query_data, **header_data}

            # 5. We assume the annotated_type has a `from_dict(...)` or similar constructor
            #    Adjust this to match your typed model's constructor pattern (Pydantic, etc.)
            if not hasattr(annotated_type, "from_dict"):
                raise AttributeError(f"Type '{annotated_type.__name__}' does not have a 'from_dict' method.")

            # 6. Convert the JSON to a strongly typed model
            #    Using Pydantic's parse_obj or constructor
            typed_obj = annotated_type.from_dict(merged_data)

            # 7. Replace the first argument with the typed object
            new_args = (typed_obj,) + args[1:]

            # 8. Call your original function with typed_obj
            result = func(*new_args, **kwargs)

            # 9. If the result has a `.to_dict()`, convert to dict so Flask can return JSON
            #    (Optional step, depending on your return-type needs.)
            if hasattr(result, "to_dict") and callable(result.to_dict):
                return result.to_dict()

            return result

        return wrapper

    return decorator
