import base64

import functions_framework
from cloudevents.http import CloudEvent
from injector import Injector

from infrastructure import LoggerStrategy, build_di_container, inject_dependency


@functions_framework.cloud_event
@inject_dependency(build_di_container())
def hello_extended_pubsub(cloud_event: CloudEvent, injector: Injector):
    logger = injector.get(LoggerStrategy)

    data = cloud_event.data  # The event's data

    # Extract the base64-encoded message, if present
    pubsub_message = data.get("message", {})
    base64_msg = pubsub_message.get("data", "")

    if base64_msg:
        message_text = base64.b64decode(base64_msg).decode("utf-8")
    else:
        message_text = "No message received"

    # Log information with our named logger
    logger.info("CloudEvent ID: %s", cloud_event["id"])
    logger.info("CloudEvent Source: %s", cloud_event["source"])
    logger.info("Pub/Sub Message: %s", message_text)
