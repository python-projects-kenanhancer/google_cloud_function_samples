import logging

from application import GreetingAppRequest, SayHelloUseCase
from cloud_functions.dtos import GreetingHttpRequest, GreetingHttpResponse
from infrastructure import SayHelloSettings, Settings, inject_logger, inject_settings_from_gcp_storage_env, inject_typed_request

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
def say_hello_ultimate_http(
    request: GreetingHttpRequest, say_hello_settings: SayHelloSettings, settings: Settings, logger: logging.Logger
):

    say_hello_use_case = SayHelloUseCase(say_hello_settings)

    request_app = GreetingAppRequest.model_validate(request.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    return GreetingHttpResponse.model_validate(greeting_message.to_dict())
