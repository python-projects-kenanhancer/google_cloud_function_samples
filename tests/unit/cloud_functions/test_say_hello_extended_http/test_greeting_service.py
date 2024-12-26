from datetime import datetime
from unittest.mock import patch

from cloud_functions.say_hello_extended_http import (
    BasicGreetingStrategy,
    GreetingService,
    GreetingStrategyFactory,
    HolidayGreetingStrategy,
    TimeBasedGreetingStrategy,
)
from schemas.say_hello_settings.greeting_language import GreetingLanguage
from schemas.say_hello_settings.greeting_type import GreetingType


class TestGreetingService:
    def test_get_greeting_message_basic_en(self):
        greeting_strategy_factory = GreetingStrategyFactory()

        greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)

        greeting_service = GreetingService(
            greeting_strategy_factory=greeting_strategy_factory,
            greeting_type=GreetingType.BASIC,
            greeting_language=GreetingLanguage.EN,
        )

        name = "Alice"
        greeting_message = greeting_service.get_greeting_message(name=name)

        assert name in greeting_message
        assert "Hello" in greeting_message

    @patch("cloud_functions.say_hello_extended_http.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_get_greeting_message_timebased_fr(self, mock_datetime):
        mock_now = datetime(2024, 12, 10, 9, 0, 0)

        mock_datetime.datetime.now.return_value = mock_now

        greeting_strategy_factory = GreetingStrategyFactory()

        greeting_strategy_factory.register(GreetingType.TIMEBASED, TimeBasedGreetingStrategy)

        greeting_service = GreetingService(
            greeting_strategy_factory=greeting_strategy_factory,
            greeting_type=GreetingType.TIMEBASED,
            greeting_language=GreetingLanguage.FR,
        )

        name = "Bob"
        greeting_message = greeting_service.get_greeting_message(name=name)

        assert name in greeting_message
        assert "Bonjour" in greeting_message

    @patch("cloud_functions.say_hello_extended_http.greeting_strategies.holiday_greeting_strategy.datetime")
    def test_get_greeting_message_holiday_es(self, mock_datetime):
        mock_now = datetime(2024, 12, 25, 10, 0, 0)
        mock_datetime.datetime.now.return_value = mock_now

        factory = GreetingStrategyFactory()
        factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)

        service = GreetingService(
            greeting_strategy_factory=factory,
            greeting_type=GreetingType.HOLIDAY,
            greeting_language=GreetingLanguage.ES,
        )

        name = "Charlie"
        message = service.get_greeting_message(name)

        assert name in message
        assert "Feliz Navidad" in message
