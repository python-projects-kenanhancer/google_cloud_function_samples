import functions_framework
from flask import Request

from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import LoggerStrategy, SayHelloSettings, build_di_container, inject_dependency


@functions_framework.http
@inject_dependency(build_di_container())
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
