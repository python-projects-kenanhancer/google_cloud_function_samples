import logging

from application import GreetingAppRequest, SayHelloUseCase
from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import (
    build_di_container,
    inject_logger,
    inject_typed_request,
)

# Parameter Object Design Pattern
# Result Object Design Pattern


injector = build_di_container()


@inject_typed_request()
@inject_logger()
def say_hello_ultimate_http(request: GreetingHttpRequest, logger: logging.Logger):

    say_hello_use_case: SayHelloUseCase = injector.get(SayHelloUseCase)

    request_app = GreetingAppRequest.model_validate(request.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message)

    return GreetingHttpResponse.model_validate(greeting_message.to_dict())
