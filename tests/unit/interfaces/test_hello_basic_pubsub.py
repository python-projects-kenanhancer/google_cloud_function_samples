import base64
from unittest.mock import MagicMock

import pytest
from cloudevents.http import CloudEvent

from infrastructure import LoggerStrategy, build_di_container
from interfaces import hello_basic_pubsub


class TestHelloBasicPubsub:
    @pytest.fixture
    def mock_logger_strategy(self):
        """
        Create a MagicMock that behaves like LoggerStrategy.
        """
        return MagicMock(spec=LoggerStrategy)

    @pytest.fixture
    def mock_injector(self, mock_logger_strategy):
        """
        Build a new DI container and override the LoggerStrategy binding with our mock.
        """
        injector = build_di_container()
        # Override the binding so that any .get(LoggerStrategy) returns our mock
        injector.binder.bind(LoggerStrategy, mock_logger_strategy)

        return injector

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
    def test_hello_pubsub(self, mock_injector, mock_logger_strategy, attributes, data, expected_id, expected_message):
        """
        Tests the hello_pubsub CloudEvent function by injecting various
        payloads and asserting the logged output matches expectations.
        """
        # Create the CloudEvent with the given attributes and data
        event = CloudEvent(attributes, data)

        # Call the function under test
        hello_basic_pubsub.__wrapped__(cloud_event=event, injector=mock_injector)

        # Assert: Verify the calls on the mock logger
        mock_logger_strategy.info.assert_any_call(f"CloudEvent ID: {attributes["id"]}")
        mock_logger_strategy.info.assert_any_call(f"CloudEvent Source: {attributes["source"]}")
        mock_logger_strategy.info.assert_any_call(f"Pub/Sub Message: {expected_message}")
