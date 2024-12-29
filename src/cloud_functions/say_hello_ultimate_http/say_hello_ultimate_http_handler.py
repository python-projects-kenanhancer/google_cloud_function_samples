import logging

from config_loaders.decorators import inject_settings_from_gcp_storage_env
from decorators import inject_logger, inject_typed_request
from domain.greeting import (
    BasicGreetingStrategy,
    GreetingService,
    GreetingStrategyFactory,
    GreetingType,
    HolidayGreetingStrategy,
    PersonName,
    SayHelloSettings,
    TimeBasedGreetingStrategy,
)
from models import Settings

from .greeting_request_response import GreetingRequest, GreetingResponse

# Parameter Object Design Pattern
# Result Object Design Pattern


@inject_typed_request()
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
def say_hello_ultimate_http_handler(
    request: GreetingRequest, say_hello_settings: SayHelloSettings, settings: Settings, logger: logging.Logger
):

    greeting_strategy_factory = GreetingStrategyFactory()

    greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.TIME_BASED, TimeBasedGreetingStrategy)

    greeting_service = GreetingService(
        greeting_strategy_factory=greeting_strategy_factory,
        greeting_type=say_hello_settings.greeting_type,
        greeting_language=say_hello_settings.greeting_language,
    )

    greeting_message = greeting_service.get_greeting_message(PersonName.model_validate(request))
    logger.info("Final greeting to user: %s", greeting_message)

    return GreetingResponse(message=greeting_message)
