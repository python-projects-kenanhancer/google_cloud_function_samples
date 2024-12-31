import logging

import functions_framework
from flask import Request

from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import SayHelloSettings, inject_settings_from_gcp_storage_env

# ---------------------------------------------------------
# Configure logging
# ---------------------------------------------------------
LOG_FORMAT = "%(asctime)s %(name)s [%(levelname)s]: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Create a named logger (instead of using the root logger)
logger = logging.getLogger(__name__)


@functions_framework.http
@inject_settings_from_gcp_storage_env(
    param_name="say_hello_settings",
    bucket_name="app-config-boilerplate",
    blob_name=".env.say_hello",
    project_id="nexum-dev-364711",
)
def say_hello_extended_http(request: Request, say_hello_settings: SayHelloSettings):
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

    say_hello_use_case = SayHelloUseCase(say_hello_settings)

    request_app = GreetingAppRequest(first_name=name, last_name="")

    greeting_message = say_hello_use_case.execute(request_app)

    return greeting_message.message
