import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask, request

from cloud_functions import say_hello_extended_http
from domain import GreetingLanguage, GreetingType
from infrastructure import LoggerStrategy, SayHelloSettings, build_di_container


class TestSayHelloExtendedHttp:
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

        mock_injector.binder.bind(
            SayHelloSettings,
            SayHelloSettings(default_name="World", greeting_type=greeting_type, greeting_language=greeting_language),
        )

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
    def test_http_function_timebased_morning(self, mock_datetime, mock_injector, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            mock_now = datetime(2024, 12, 10, 8, 0, 0)
            mock_datetime.datetime.now.return_value = mock_now

            mock_injector.binder.bind(
                SayHelloSettings,
                SayHelloSettings(
                    default_name="World!", greeting_type=GreetingType.TIME_BASED, greeting_language=GreetingLanguage.EN
                ),
            )

            say_hello_settings = mock_injector.get(SayHelloSettings)

            response: str = say_hello_extended_http(request, say_hello_settings)

        assert isinstance(response, str)
        assert "MorningUser" in response
        assert "Good morning" in response

    def test_http_function_timebased_morning_v2(self, flask_app):
        with flask_app.test_request_context("/?name=MorningUser", method="GET"):
            with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:
                mock_now = datetime(2024, 12, 10, 8, 0, 0)
                mock_datetime.datetime.now.return_value = mock_now

                response: str = say_hello_extended_http(request=request)

        assert isinstance(response, str)
        assert "MorningUser" in response
        assert "Good morning" in response
