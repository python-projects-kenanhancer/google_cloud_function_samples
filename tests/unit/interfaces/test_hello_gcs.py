from unittest.mock import MagicMock

import pytest
from cloudevents.http import CloudEvent

from infrastructure import LoggerStrategy, build_di_container
from interfaces import hello_basic_gcs


class TestHelloGcs:
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

    def test_hello_gcs_prints_details(self, mock_injector, mock_logger_strategy):
        """
        Ensures that hello_basic_gcs prints the correct details when
        triggered by a CloudEvent with relevant data.
        """
        # Define CloudEvent attributes
        attributes = {
            "id": "1234-1234-1234",
            "source": "//storage.googleapis.com/projects/_/buckets/my-bucket",
            "specversion": "1.0",
            "type": "google.cloud.storage.object.v1.finalized",
        }

        # Define CloudEvent data payload
        data = {
            "bucket": "my-bucket",
            "name": "file.txt",
            "metageneration": "1",
            "timeCreated": "2021-04-23T07:00:00.000Z",
            "updated": "2021-04-23T07:00:00.000Z",
        }

        # Create the CloudEvent
        event = CloudEvent(attributes, data)

        # Invoke the function
        hello_basic_gcs.__wrapped__(cloud_event=event, injector=mock_injector)

        # Assert: Verify the calls on the mock logger
        mock_logger_strategy.info.assert_any_call(f"Event ID: {attributes["id"]}")
        mock_logger_strategy.info.assert_any_call(f"Event type: {attributes["type"]}")
        mock_logger_strategy.info.assert_any_call(f"Bucket: {data['bucket']}")
