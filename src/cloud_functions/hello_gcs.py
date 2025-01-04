import functions_framework
from cloudevents.http import CloudEvent
from injector import Injector

from infrastructure import LoggerStrategy, build_di_container, inject_injector


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
@inject_injector(build_di_container())
def hello_gcs(cloud_event: CloudEvent, injector: Injector):
    logger = injector.get(LoggerStrategy)

    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    logger.info(f"Event ID: {event_id}")
    logger.info(f"Event type: {event_type}")
    logger.info(f"Bucket: {bucket}")
    logger.info(f"File: {name}")
    logger.info(f"Metageneration: {metageneration}")
    logger.info(f"Created: {timeCreated}")
    logger.info(f"Updated: {updated}")
