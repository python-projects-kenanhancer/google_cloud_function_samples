from injector import Injector

from application import GreetingAppRequest, SayHelloUseCase
from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import LoggerStrategy, SayHelloSettings, Settings, build_di_container, inject_dependency, inject_typed_request

# Parameter Object Design Pattern
# Result Object Design Pattern


@inject_typed_request()
@inject_dependency(build_di_container())
def say_hello_ultimate_http(
    request: GreetingHttpRequest,
    say_hello_use_case: SayHelloUseCase,
    logger: LoggerStrategy,
    injector: Injector,
    settings: Settings,
    say_hello_settings: SayHelloSettings,
):

    settings_v2 = injector.get(Settings)

    say_hello_settings_v2 = injector.get(SayHelloSettings)

    print(settings == settings_v2)

    print(say_hello_settings == say_hello_settings_v2)

    request_app = GreetingAppRequest.model_validate(request.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message.message)

    return GreetingHttpResponse.model_validate(greeting_message.to_dict())
