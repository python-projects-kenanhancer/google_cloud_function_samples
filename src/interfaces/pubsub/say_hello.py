from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import (
    GcpPubSubCloudEvent,
    GcpPubSubEventData,
    LoggerStrategy,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_cloud_event_middleware,
)
from interfaces.dtos import GreetingMessage


# Triggered by a change in a storage bucket
@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_cloud_event_middleware,
    logger_middleware,
    time_middleware,
)
def say_hello(cloud_event: GcpPubSubCloudEvent[GreetingMessage], say_hello_use_case: SayHelloUseCase, logger: LoggerStrategy):

    data: GcpPubSubEventData[GreetingMessage] = cloud_event.data  # The event's data

    # Extract the base64-encoded message, if present
    pubsub_data: GreetingMessage = data.message.data

    # Log information with our named logger
    logger.info("CloudEvent ID: %s", cloud_event.id)
    logger.info("CloudEvent Source: %s", cloud_event.source)
    logger.info("Pub/Sub Message: %s", pubsub_data.model_dump_json())

    request_app = GreetingAppRequest.model_validate(pubsub_data.to_dict())

    greeting_message = say_hello_use_case.execute(request_app)

    logger.info(greeting_message.message)
