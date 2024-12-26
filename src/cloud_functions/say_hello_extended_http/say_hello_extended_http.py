import logging

import functions_framework
from flask import Request

from config_loaders import inject_settings_from_gcp_storage_env
from schemas import GreetingType, SayHelloSettings

from .greeting_service import GreetingService
from .greeting_strategies import BasicGreetingStrategy, HolidayGreetingStrategy, TimeBasedGreetingStrategy
from .greeting_strategy_factory import GreetingStrategyFactory

# ---------------------------------------------------------
# Configure logging
# ---------------------------------------------------------
LOG_FORMAT = "%(asctime)s %(name)s [%(levelname)s]: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Create a named logger (instead of using the root logger)
logger = logging.getLogger(__name__)


@functions_framework.http
@inject_settings_from_gcp_storage_env(
    bucket_name="app-config-boilerplate", blob_name=".env.say_hello", project_id="nexum-dev-364711"
)
def say_hello_extended_http(request: Request, settings: SayHelloSettings):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
        logger.info("Name found in JSON: %s", name)
    elif request_args and "name" in request_args:
        name = request_args["name"]
        logger.info("Name found in query params: %s", name)
    else:
        name = settings.default_name
        logger.info("Name not provided, using default: %s", name)

    greeting_strategy_factory = GreetingStrategyFactory.default()

    greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.TIMEBASED, TimeBasedGreetingStrategy)

    greeting_service = GreetingService(
        greeting_strategy_factory=greeting_strategy_factory,
        greeting_type=settings.greeting_type,
        greeting_language=settings.greeting_language,
    )

    greeting_message = greeting_service.get_greeting_message(name=name)
    logger.info("Final greeting to user: %s", greeting_message)

    return greeting_message
