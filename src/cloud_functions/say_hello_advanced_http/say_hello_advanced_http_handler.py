import functions_framework

from .greeting_request_response import GreetingRequest, GreetingResponse

# Parameter Object Design Pattern
# Result Object Design Pattern


@functions_framework.typed
def say_hello_advanced_http_handler(req: GreetingRequest):
    full_name = f"{req.first_name} {req.last_name}"
    return GreetingResponse(message=f"Hello {full_name}!")
