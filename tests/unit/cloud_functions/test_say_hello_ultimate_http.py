from datetime import datetime
from unittest.mock import patch

import pytest
from flask import Flask

from cloud_functions.say_hello_ultimate_http import GreetingRequest, GreetingResponse, say_hello_ultimate_http_handler
from domain.greeting import GreetingLanguage, GreetingType, SayHelloSettings


class TestSayHelloUltimateHttp:
    @pytest.fixture
    def flask_app(self):
        return Flask(__name__)

    @pytest.mark.parametrize(
        "greeting_type, greeting_language, first_name, last_name, expected_keywords",
        [
            (GreetingType.BASIC, GreetingLanguage.EN, "John", "Doe", ["Hello", "John Doe"]),
            (GreetingType.HOLIDAY, GreetingLanguage.EN, "Alice", "Smith", ["Happy Holidays", "Alice Smith"]),
            # For TIME_BASED, you might expect different results (e.g., "Good morning" / "Good afternoon"),
            # so here we just check that the message contains "Good".
            (GreetingType.TIME_BASED, GreetingLanguage.EN, "Bob", "Marley", ["Good", "Bob Marley"]),
        ],
    )
    def test_say_hello_ultimate_http(self, flask_app, greeting_type, greeting_language, first_name, last_name, expected_keywords):
        """
        Tests the say_hello_ultimate_http_handler function with different greeting types.
        The test verifies that the returned greeting message contains expected keywords.
        """

        with flask_app.test_request_context(
            "/",
            method="POST",
            data={"first_name": first_name, "last_name": last_name},
            content_type="application/json",
        ):
            greeting_request = GreetingRequest(first_name=first_name, last_name=last_name)

            # Mock settings
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=greeting_type,
                greeting_language=greeting_language,
            )

            # Act: Call the function under test
            response: GreetingResponse = say_hello_ultimate_http_handler.__wrapped__(
                request=greeting_request, say_hello_settings=fake_settings
            )

        # Assert: Check the result type and that the expected keywords are in the message
        assert isinstance(response, GreetingResponse)
        for keyword in expected_keywords:
            assert keyword in response.message, f"Expected '{keyword}' to be in greeting message"

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_http_function_timebased_morning(self, mock_datetime, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            greeting_request = GreetingRequest(first_name="John", last_name="Doe")
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=GreetingType.TIME_BASED,
                greeting_language=GreetingLanguage.EN,
            )
            mock_now = datetime(2024, 12, 10, 8, 0, 0)
            mock_datetime.datetime.now.return_value = mock_now

            response: GreetingResponse = say_hello_ultimate_http_handler.__wrapped__(
                request=greeting_request, say_hello_settings=fake_settings
            )
            assert "John Doe" in response.message
            assert "Good morning" in response.message

    def test_http_function_timebased_morning_v2(self, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=GreetingType.TIME_BASED,
                greeting_language=GreetingLanguage.EN,
            )
            with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:
                greeting_request = GreetingRequest(first_name="Alice", last_name="Smith")
                mock_now = datetime(2024, 12, 10, 8, 0, 0)
                mock_datetime.datetime.now.return_value = mock_now

                response: GreetingResponse = say_hello_ultimate_http_handler.__wrapped__(
                    request=greeting_request, say_hello_settings=fake_settings
                )
                assert "Alice Smith" in response.message
                assert "Good morning" in response.message
