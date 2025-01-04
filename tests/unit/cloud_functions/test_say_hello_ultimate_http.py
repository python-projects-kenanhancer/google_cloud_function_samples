from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from cloud_functions import GreetingHttpRequest, GreetingHttpResponse, say_hello_ultimate_http
from domain import GreetingLanguage, GreetingType
from infrastructure import LoggerStrategy, SayHelloSettings, build_di_container


class TestSayHelloUltimateHttp:
    @pytest.fixture
    def flask_app(self):
        return Flask(__name__)

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
        "greeting_type, greeting_language, first_name, last_name, mock_now, datetime_patch, expected_keywords",
        [
            (GreetingType.BASIC, GreetingLanguage.EN, "John", "Doe", None, None, ["Hello", "John Doe"]),
            (
                GreetingType.HOLIDAY,
                GreetingLanguage.EN,
                "Bob",
                "Marley",
                datetime(2024, 12, 10, 8, 0, 0),
                "domain.greeting.greeting_strategies.holiday_greeting_strategy.datetime",
                ["Happy Holidays", "Bob Marley"],
            ),
            (
                GreetingType.TIME_BASED,
                GreetingLanguage.EN,
                "Bob",
                "Marley",
                datetime(2024, 12, 10, 14, 0, 0),
                "domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime",
                ["Good afternoon", "Bob Marley"],
            ),
        ],
    )
    def test_say_hello_ultimate_http(
        self,
        mock_injector,
        flask_app,
        greeting_type,
        greeting_language,
        first_name,
        last_name,
        mock_now,
        datetime_patch,
        expected_keywords,
    ):

        mock_injector.binder.bind(
            SayHelloSettings,
            SayHelloSettings(default_name="World", greeting_type=greeting_type, greeting_language=greeting_language),
        )

        with flask_app.test_request_context(
            "/",
            method="POST",
            data={"first_name": first_name, "last_name": last_name},
            content_type="application/json",
        ):
            if datetime_patch:
                with patch(datetime_patch) as mock_datetime:
                    mock_datetime.datetime.now.return_value = mock_now
                    greeting_request = GreetingHttpRequest(first_name=first_name, last_name=last_name)
                    response: GreetingHttpResponse = say_hello_ultimate_http.__wrapped__(
                        request=greeting_request, injector=mock_injector
                    )
            else:
                # No patch needed for this scenario
                greeting_request = GreetingHttpRequest(first_name=first_name, last_name=last_name)
                response: GreetingHttpResponse = say_hello_ultimate_http.__wrapped__(
                    request=greeting_request, injector=mock_injector
                )

        # Assert: Check the result type and that the expected keywords are in the message
        assert isinstance(response, GreetingHttpResponse)
        for keyword in expected_keywords:
            assert keyword in response.message, f"Expected '{keyword}' to be in greeting message"

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_http_function_timebased_morning(self, mock_datetime, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):

            mock_now = datetime(2024, 12, 10, 8, 0, 0)
            mock_datetime.datetime.now.return_value = mock_now

            greeting_request = GreetingHttpRequest(first_name="John", last_name="Doe")

            response: GreetingHttpResponse = say_hello_ultimate_http.__wrapped__(request=greeting_request)

        assert isinstance(response, GreetingHttpResponse)
        assert "John Doe" in response.message
        assert "Good morning" in response.message

    def test_http_function_timebased_morning_v2(self, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):

            with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:

                mock_now = datetime(2024, 12, 10, 8, 0, 0)
                mock_datetime.datetime.now.return_value = mock_now

                greeting_request = GreetingHttpRequest(first_name="Alice", last_name="Smith")

                response: GreetingHttpResponse = say_hello_ultimate_http.__wrapped__(request=greeting_request)

        assert isinstance(response, GreetingHttpResponse)
        assert "Alice Smith" in response.message
        assert "Good morning" in response.message
