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


# Triggered by a change in a storage bucket
@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_cloud_event_middleware,
    logger_middleware,
    time_middleware,
)
def hello_extended_pubsub(cloud_event: GcpPubSubCloudEvent[str], logger: LoggerStrategy):

    data = cloud_event.data  # The event's data

    data_message = data.message

    pubsub_message = data_message.data or "No message received"

    # Log information with our named logger
    logger.info("CloudEvent ID: %s", cloud_event.id)
    logger.info("CloudEvent Source: %s", cloud_event.source)
    logger.info("Pub/Sub Message: %s", pubsub_message)
