import base64

import functions_framework
from cloudevents.http import CloudEvent
from injector import Injector

from infrastructure import LoggerStrategy, build_di_container, inject_dependency


@functions_framework.cloud_event
@inject_dependency(build_di_container())
def hello_basic_pubsub(cloud_event: CloudEvent, injector: Injector):
    logger = injector.get(LoggerStrategy)

    data = cloud_event.data

    # Safely extract the base64-encoded message
    message_fields = data.get("message", {})
    base64_msg = message_fields.get("data", "")

    # Decode the Pub/Sub message from base64
    if base64_msg:
        message_text = base64.b64decode(base64_msg).decode("utf-8")
    else:
        message_text = "No message received"

    logger.info(f"CloudEvent ID: {cloud_event['id']}")
    logger.info(f"CloudEvent Source: {cloud_event['source']}")
    logger.info(f"Pub/Sub Message: {message_text}")
