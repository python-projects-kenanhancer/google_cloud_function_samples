import functions_framework

from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse

# Parameter Object Design Pattern
# Result Object Design Pattern


@functions_framework.typed
def say_hello_advanced_http(req: GreetingHttpRequest):
    full_name = f"{req.first_name} {req.last_name}"
    return GreetingHttpResponse(message=f"Hello {full_name}!")
