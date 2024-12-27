import logging

import functions_framework
from flask import Request

from config_loaders import inject_settings_from_gcp_storage_env
from decorators import inject_logger
from schemas import GreetingType, SayHelloSettings, Settings

from .greeting_service import GreetingService
from .greeting_strategies import BasicGreetingStrategy, HolidayGreetingStrategy, TimeBasedGreetingStrategy
from .greeting_strategy_factory import GreetingStrategyFactory


@functions_framework.http
@inject_logger()
@inject_settings_from_gcp_storage_env(
    param_name="say_hello_settings",
    bucket_name="app-config-boilerplate",
    blob_name=".env.say_hello",
    project_id="nexum-dev-364711",
)
@inject_settings_from_gcp_storage_env(
    param_name="settings",
    bucket_name="app-config-boilerplate",
    blob_name=".env",
    project_id="nexum-dev-364711",
)
def say_hello_extended_http(request: Request, say_hello_settings: SayHelloSettings, settings: Settings, logger: logging.Logger):
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

    greeting_strategy_factory = GreetingStrategyFactory.default()

    greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.TIMEBASED, TimeBasedGreetingStrategy)

    greeting_service = GreetingService(
        greeting_strategy_factory=greeting_strategy_factory,
        greeting_type=say_hello_settings.greeting_type,
        greeting_language=say_hello_settings.greeting_language,
    )

    greeting_message = greeting_service.get_greeting_message(name=name)
    logger.info("Final greeting to user: %s", greeting_message)

    return greeting_message
