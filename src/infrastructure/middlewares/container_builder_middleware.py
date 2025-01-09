from infrastructure import Context, Next

from ..dependency_injection_configurations import build_di_container


def container_builder_middleware(context: Context, next: Next):
    if "injector" not in context.kwargs:
        container = build_di_container()
        context.kwargs["injector"] = container
    return next()
