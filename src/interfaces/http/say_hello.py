from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import (
    LoggerStrategy,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_request_middleware,
)
from interfaces.dtos import GreetingHttpRequest, GreetingHttpResponse

# Parameter Object Design Pattern
# Result Object Design Pattern


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    logger_middleware,
    time_middleware,
)
def say_hello(
    request: GreetingHttpRequest,
    say_hello_use_case: SayHelloUseCase,
    logger: LoggerStrategy,
):

    request_app = GreetingAppRequest.model_validate(request.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message.message)

    return GreetingHttpResponse.model_validate(greeting_message.to_dict())
