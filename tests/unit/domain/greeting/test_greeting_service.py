from datetime import datetime
from unittest.mock import patch

from domain import (
    BasicGreetingStrategy,
    GreetingLanguage,
    GreetingService,
    GreetingStrategyFactory,
    GreetingType,
    HolidayGreetingStrategy,
    PersonName,
    TimeBasedGreetingStrategy,
)


class TestGreetingService:
    def test_get_greeting_message_basic_en(self):
        greeting_strategy_factory = GreetingStrategyFactory()

        greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)

        greeting_service = GreetingService(
            greeting_strategy_factory=greeting_strategy_factory,
            greeting_type=GreetingType.BASIC,
            greeting_language=GreetingLanguage.EN,
        )

        first_name = "Alice"
        last_name = "Smith"
        greeting_message = greeting_service.get_greeting_message(PersonName(first_name=first_name, last_name=last_name))

        assert f"{first_name} {last_name}" in greeting_message
        assert "Hello" in greeting_message

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_get_greeting_message_timebased_fr(self, mock_datetime):
        mock_now = datetime(2024, 12, 10, 9, 0, 0)

        mock_datetime.datetime.now.return_value = mock_now

        greeting_strategy_factory = GreetingStrategyFactory()

        greeting_strategy_factory.register(GreetingType.TIME_BASED, TimeBasedGreetingStrategy)

        greeting_service = GreetingService(
            greeting_strategy_factory=greeting_strategy_factory,
            greeting_type=GreetingType.TIME_BASED,
            greeting_language=GreetingLanguage.FR,
        )

        first_name = "Bob"
        last_name = "Doe"
        greeting_message = greeting_service.get_greeting_message(PersonName(first_name=first_name, last_name=last_name))

        assert f"{first_name} {last_name}" in greeting_message
        assert "Bonjour" in greeting_message

    @patch("domain.greeting.greeting_strategies.holiday_greeting_strategy.datetime")
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

        first_name = "Charlie"
        last_name = "Brown"
        message = service.get_greeting_message(PersonName(first_name=first_name, last_name=last_name))

        assert f"{first_name} {last_name}" in message
        assert "Feliz Navidad" in message
