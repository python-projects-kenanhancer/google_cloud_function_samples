import json
from datetime import datetime
from unittest.mock import patch

import pytest
from flask import Flask, request

from cloud_functions import say_hello_extended_http
from domain.greeting import GreetingLanguage, GreetingType, SayHelloSettings


class TestSayHelloExtendedHttp:
    @pytest.fixture
    def flask_app(self):
        return Flask(__name__)

    @pytest.mark.parametrize(
        "greeting_type,greeting_language,json_payload,query_string,expected_name",
        [
            (GreetingType.BASIC, GreetingLanguage.EN, {"name": "Alice"}, "", "Alice"),
            (GreetingType.TIME_BASED, GreetingLanguage.FR, None, "?name=Bob", "Bob"),
            (GreetingType.HOLIDAY, GreetingLanguage.ES, None, "", "World"),  # fallback
        ],
    )
    def test_http_function(self, flask_app, greeting_type, greeting_language, json_payload, query_string, expected_name):
        method = "POST" if json_payload else "GET"
        data = json.dumps(json_payload) if json_payload else None

        with flask_app.test_request_context(
            f"/{query_string}",
            method=method,
            data=data,
            content_type="application/json" if json_payload else None,
        ):
            # Mock settings
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=greeting_type,
                greeting_language=greeting_language,
            )

            # Call the original/undecorated function:
            response = say_hello_extended_http.__wrapped__(request=request, say_hello_settings=fake_settings)
            assert expected_name in response

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_http_function_timebased_morning(self, mock_datetime, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=GreetingType.TIME_BASED,
                greeting_language=GreetingLanguage.EN,
            )
            mock_now = datetime(2024, 12, 10, 8, 0, 0)
            mock_datetime.datetime.now.return_value = mock_now

            response = say_hello_extended_http.__wrapped__(request=request, say_hello_settings=fake_settings)
            assert "MorningUser" in response
            assert "Good morning" in response

    def test_http_function_timebased_morning_v2(self, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            fake_settings = SayHelloSettings(
                default_name="World",
                greeting_type=GreetingType.TIME_BASED,
                greeting_language=GreetingLanguage.EN,
            )
            with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:
                mock_now = datetime(2024, 12, 10, 8, 0, 0)
                mock_datetime.datetime.now.return_value = mock_now

                response = say_hello_extended_http.__wrapped__(request=request, say_hello_settings=fake_settings)
                assert "MorningUser" in response
                assert "Good morning" in response
