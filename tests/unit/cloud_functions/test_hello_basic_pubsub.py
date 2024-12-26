import base64

import pytest
from cloudevents.http import CloudEvent

from cloud_functions import hello_basic_pubsub


class TestHelloBasicPubsub:
    @pytest.mark.parametrize(
        "attributes, data, expected_id, expected_message",
        [
            # 1) Basic message test
            (
                {
                    "id": "basic-message-1234",
                    "source": "//pubsub.googleapis.com/projects/YOUR_PROJECT/topics/YOUR_TOPIC",
                    "specversion": "1.0",
                    "type": "google.cloud.pubsub.topic.v1.messagePublished",
                },
                {
                    "message": {
                        "data": base64.b64encode("Hello, Pub_Sub".encode()).decode(),
                        "messageId": "abc-123",
                        "attributes": {
                            "author": "John Doe",
                            "priority": "high",
                        },
                    }
                },
                "basic-message-1234",
                "Hello, Pub_Sub",
            ),
            # 2) Empty data field
            (
                {
                    "id": "empty-data-test",
                    "source": "//pubsub.googleapis.com/projects/YOUR_PROJECT/topics/empty-topic",
                    "specversion": "1.0",
                    "type": "google.cloud.pubsub.topic.v1.messagePublished",
                },
                {
                    "message": {
                        "data": "",
                        "messageId": "empty-456",
                    }
                },
                "empty-data-test",
                "No message received",
            ),
            # 3) Large message example
            (
                {
                    "id": "large-message-001",
                    "source": "//pubsub.googleapis.com/projects/YOUR_PROJECT/topics/large-topic",
                    "specversion": "1.0",
                    "type": "google.cloud.pubsub.topic.v1.messagePublished",
                },
                {
                    "message": {
                        "data": base64.b64encode(b"This is a longer message to test capacity. Hello Global.").decode(),
                        "messageId": "large-789",
                    }
                },
                "large-message-001",
                "This is a longer message to test capacity. Hello Global.",
            ),
        ],
    )
    def test_hello_pubsub(self, capsys, attributes, data, expected_id, expected_message):
        """
        Tests the hello_pubsub CloudEvent function by injecting various
        payloads and asserting the logged output matches expectations.
        """
        # Create the CloudEvent with the given attributes and data
        event = CloudEvent(attributes, data)

        # Call the function under test
        hello_basic_pubsub(event)

        # Capture the logs printed to stdout
        captured = capsys.readouterr()
        output = captured.out

        # Assert the expected logs are present
        assert f"CloudEvent ID: {expected_id}" in output
        assert f"Pub/Sub Message: {expected_message}" in output

        # Optional: You could also test other log lines, e.g.:
        # assert f"CloudEvent Source: {attributes['source']}" in output
