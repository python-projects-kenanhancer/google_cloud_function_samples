import base64

import functions_framework
from cloudevents.http import CloudEvent


@functions_framework.cloud_event
def hello_basic_pubsub(cloud_event: CloudEvent):
    # The CloudEvent "data" contains Pub/Sub message data,
    # typically as { "message": { "data": "base64-encoded-string" }, ... }
    event_data = cloud_event.data

    # Safely extract the base64-encoded message
    message_fields = event_data.get("message", {})
    base64_msg = message_fields.get("data", "")

    # Decode the Pub/Sub message from base64
    if base64_msg:
        message_text = base64.b64decode(base64_msg).decode("utf-8")
    else:
        message_text = "No message received"

    print(f"CloudEvent ID: {cloud_event['id']}")
    print(f"CloudEvent Source: {cloud_event['source']}")
    print(f"Pub/Sub Message: {message_text}")
