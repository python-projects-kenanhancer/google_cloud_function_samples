from injector import Injector

from infrastructure import (
    GCSCloudEvent,
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
def hello_extended_gcs(cloud_event: GCSCloudEvent, injector: Injector):
    logger = injector.get(LoggerStrategy)

    data = cloud_event.data

    event_id = cloud_event.id
    event_type = cloud_event.type

    bucket = data.bucket
    name = data.name
    metageneration = data.metageneration
    timeCreated = data.timeCreated
    updated = data.updated

    logger.info(f"Event ID: {event_id}")
    logger.info(f"Event type: {event_type}")
    logger.info(f"Bucket: {bucket}")
    logger.info(f"File: {name}")
    logger.info(f"Metageneration: {metageneration}")
    logger.info(f"Created: {timeCreated}")
    logger.info(f"Updated: {updated}")
