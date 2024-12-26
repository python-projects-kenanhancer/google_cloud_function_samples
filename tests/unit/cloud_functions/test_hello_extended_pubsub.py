import logging

import pytest
from cloudevents.http import CloudEvent

from cloud_functions import hello_extended_pubsub


class TestHelloPubsub:
    @pytest.mark.parametrize(
        "base64_input, expected_message",
        [
            (b"SGVsbG8gV29ybGQ=", "Hello World"),  # "Hello World" in base64
            (b"", "No message received"),  # Test empty data
        ],
    )
    def test_hello_pubsub(self, caplog, base64_input, expected_message):
        # Arrange: Create CloudEvent attributes and data
        attributes = {
            "id": "test-id-1234",
            "source": "//pubsub.googleapis.com/projects/YOUR_PROJECT/topics/test-topic",
            "specversion": "1.0",
            "type": "google.cloud.pubsub.topic.v1.messagePublished",
        }
        data = {
            "message": {
                # Convert the raw bytes to a base64 string
                "data": base64_input.decode(),
            }
        }
        event = CloudEvent(attributes, data)

        # Act: Call the function under test
        # Use caplog.at_level to capture logs from your named logger
        with caplog.at_level(logging.INFO, logger="cloud_functions.hello_extended_pubsub"):
            hello_extended_pubsub(event)

        # Assert: Check that the log messages contain the expected content
        # caplog.records is a list of all log records captured
        log_messages = [record.getMessage() for record in caplog.records]

        # The function logs three lines: CloudEvent ID, Source, and Pub/Sub Message
        assert any(f"CloudEvent ID: {attributes['id']}" in msg for msg in log_messages)
        assert any(f"CloudEvent Source: {attributes['source']}" in msg for msg in log_messages)
        assert any(f"Pub/Sub Message: {expected_message}" in msg for msg in log_messages)
