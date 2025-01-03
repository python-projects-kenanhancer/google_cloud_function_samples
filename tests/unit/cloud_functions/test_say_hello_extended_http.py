import json
from datetime import datetime
from unittest.mock import patch

import pytest
from flask import Flask, request

from cloud_functions import say_hello_extended_http
from domain import GreetingLanguage, GreetingType
from infrastructure import FakeSayHelloSettingsModule, build_di_container


class TestSayHelloExtendedHttp:
    @pytest.fixture
    def flask_app(self):
        return Flask(__name__)

    @pytest.mark.parametrize(
        "greeting_type, greeting_language, json_payload, query_string, mock_now, datetime_patch, expected_name",
        [
            (GreetingType.BASIC, GreetingLanguage.EN, {"name": "Alice"}, "", None, None, "Alice"),
            (
                GreetingType.HOLIDAY,
                GreetingLanguage.ES,
                None,
                "",
                datetime(2024, 12, 10, 8, 0, 0),
                "domain.greeting.greeting_strategies.holiday_greeting_strategy.datetime",
                "World",
            ),
            (
                GreetingType.TIME_BASED,
                GreetingLanguage.FR,
                None,
                "?name=Bob",
                datetime(2024, 12, 10, 8, 0, 0),
                "domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime",
                "Bob",
            ),
        ],
    )
    @patch("cloud_functions.say_hello_extended_http.injector")
    def test_http_function(
        self,
        mock_injector,
        flask_app,
        greeting_type,
        greeting_language,
        json_payload,
        query_string,
        mock_now,
        datetime_patch,
        expected_name,
    ):
        method = "POST" if json_payload else "GET"
        data = json.dumps(json_payload) if json_payload else None

        # 1. Create a new test container or mock
        test_injector = build_di_container(
            [FakeSayHelloSettingsModule(greeting_type=greeting_type, greeting_language=greeting_language)]
        )
        # 2. Patch the global injector reference
        mock_injector.get.side_effect = test_injector.get

        with flask_app.test_request_context(
            f"/{query_string}",
            method=method,
            data=data,
            content_type="application/json" if json_payload else None,
        ):
            if datetime_patch:
                with patch(datetime_patch) as mock_datetime:
                    mock_datetime.datetime.now.return_value = mock_now
                    response: str = say_hello_extended_http(request)
            else:
                # No patch needed for this scenario
                response: str = say_hello_extended_http(request)

        assert isinstance(response, str)
        assert expected_name in response

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_http_function_timebased_morning(self, mock_datetime, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            mock_now = datetime(2024, 12, 10, 8, 0, 0)
            mock_datetime.datetime.now.return_value = mock_now

            response: str = say_hello_extended_http.__wrapped__(request=request)
            assert isinstance(response, str)
            assert "MorningUser" in response
            assert "Good morning" in response

    def test_http_function_timebased_morning_v2(self, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:
                mock_now = datetime(2024, 12, 10, 8, 0, 0)
                mock_datetime.datetime.now.return_value = mock_now

                response: str = say_hello_extended_http.__wrapped__(request=request)
                assert isinstance(response, str)
                assert "MorningUser" in response
                assert "Good morning" in response
