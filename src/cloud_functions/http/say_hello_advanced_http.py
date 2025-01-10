from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import (
    LoggerStrategy,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_request_middleware,
)

# Parameter Object Design Pattern
# Result Object Design Pattern


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    logger_middleware,
    time_middleware,
)
def say_hello_advanced_http(req: GreetingHttpRequest, logger: LoggerStrategy):

    full_name = f"{req.first_name} {req.last_name}"

    response = GreetingHttpResponse(message=f"Hello {full_name}!")

    logger.info(response.message)

    return response
