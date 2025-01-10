from datetime import datetime

from pydantic import BaseModel

from infrastructure import (
    GcpPubSubCloudEvent,
    LoggerStrategy,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_cloud_event_middleware,
)


class UserMessage(BaseModel):
    user_id: str
    action: str
    timestamp: datetime


# Triggered by a change in a storage bucket
@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_cloud_event_middleware,
    logger_middleware,
    time_middleware,
)
def hello_advanced_pubsub(cloud_event: GcpPubSubCloudEvent[UserMessage], logger: LoggerStrategy):

    data = cloud_event.data  # The event's data

    # Extract the base64-encoded message, if present
    pubsub_data = data.message.data

    # Log information with our named logger
    logger.info("CloudEvent ID: %s", cloud_event.id)
    logger.info("CloudEvent Source: %s", cloud_event.source)
    logger.info("Pub/Sub Message: %s", pubsub_data)
