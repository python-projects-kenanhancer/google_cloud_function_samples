import functions_framework
from injector import Injector

from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import LoggerStrategy, build_di_container, inject_injector

# Parameter Object Design Pattern
# Result Object Design Pattern


@functions_framework.typed
@inject_injector(build_di_container())
def say_hello_advanced_http(req: GreetingHttpRequest, injector: Injector):

    logger = injector.get(LoggerStrategy)

    full_name = f"{req.first_name} {req.last_name}"

    response = GreetingHttpResponse(message=f"Hello {full_name}!")

    logger.info(response.message)

    return response
