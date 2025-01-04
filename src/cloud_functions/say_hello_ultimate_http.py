from injector import Injector

from application import GreetingAppRequest, SayHelloUseCase
from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import LoggerStrategy, build_di_container, inject_injector, inject_typed_request

# Parameter Object Design Pattern
# Result Object Design Pattern


@inject_typed_request()
@inject_injector(build_di_container())
def say_hello_ultimate_http(request: GreetingHttpRequest, injector: Injector):

    logger = injector.get(LoggerStrategy)

    say_hello_use_case: SayHelloUseCase = injector.get(SayHelloUseCase)

    request_app = GreetingAppRequest.model_validate(request.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message.message)

    return GreetingHttpResponse.model_validate(greeting_message.to_dict())
