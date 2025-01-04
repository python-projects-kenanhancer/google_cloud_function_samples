from unittest.mock import MagicMock

import pytest
from cloudevents.http import CloudEvent

from cloud_functions import hello_extended_pubsub
from infrastructure import LoggerStrategy, build_di_container


class TestHelloPubsub:
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
        "base64_input, expected_message",
        [
            (b"SGVsbG8gV29ybGQ=", "Hello World"),  # "Hello World" in base64
            (b"", "No message received"),  # Test empty data
        ],
    )
    def test_hello_pubsub(self, mock_injector, mock_logger_strategy, base64_input, expected_message):
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

        hello_extended_pubsub.__wrapped__(cloud_event=event, injector=mock_injector)

        # Assert: Verify the calls on the mock logger
        mock_logger_strategy.info.assert_any_call("CloudEvent ID: %s", attributes["id"])
        mock_logger_strategy.info.assert_any_call("CloudEvent Source: %s", attributes["source"])
        mock_logger_strategy.info.assert_any_call("Pub/Sub Message: %s", expected_message)
