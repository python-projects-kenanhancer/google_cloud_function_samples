from config_loaders.decorators import inject_settings_from_gcp_storage_env
from decorators import inject_typed_request
from schemas import GreetingRequest, GreetingResponse, GreetingType, PersonName, SayHelloSettings, Settings

from .greeting_service import GreetingService
from .greeting_strategies import BasicGreetingStrategy, HolidayGreetingStrategy, TimeBasedGreetingStrategy
from .greeting_strategy_factory import GreetingStrategyFactory

# Parameter Object Design Pattern
# Result Object Design Pattern


@inject_typed_request()
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
def say_hello_ultimate_http(req: GreetingRequest, say_hello_settings: SayHelloSettings, settings: Settings):

    greeting_strategy_factory = GreetingStrategyFactory()

    greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
    greeting_strategy_factory.register(GreetingType.TIMEBASED, TimeBasedGreetingStrategy)

    greeting_service = GreetingService(
        greeting_strategy_factory=greeting_strategy_factory,
        greeting_type=say_hello_settings.greeting_type,
        greeting_language=say_hello_settings.greeting_language,
    )

    greeting_message = greeting_service.get_greeting_message(PersonName.model_validate(req))

    return GreetingResponse(message=greeting_message)
