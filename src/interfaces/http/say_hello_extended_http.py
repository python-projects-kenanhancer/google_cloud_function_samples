from flask import Request

from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import (
    LoggerStrategy,
    SayHelloSettings,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_request_middleware,
)


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    logger_middleware,
    time_middleware,
)
def say_hello_extended_http(
    request: Request, say_hello_settings: SayHelloSettings, say_hello_use_case: SayHelloUseCase, logger: LoggerStrategy
):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
        logger.info("Name found in JSON: %s", name)
    elif request_args and "name" in request_args:
        name = request_args["name"]
        logger.info("Name found in query params: %s", name)
    else:
        name = say_hello_settings.default_name
        logger.info("Name not provided, using default: %s", name)

    request_app = GreetingAppRequest(first_name=name, last_name="")

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message.message)

    return greeting_message.message
