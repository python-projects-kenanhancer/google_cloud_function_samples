from cloud_functions.say_hello_extended_http import BasicGreetingStrategy, GreetingStrategyFactory, HolidayGreetingStrategy
from schemas.say_hello_settings.greeting_type import GreetingType


class TestGreetingStrategyFactory:
    def test_greeting_strategy_factory_register_and_create(self):
        greeting_factory = GreetingStrategyFactory()

        greeting_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
        greeting_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)

        basic_greeting_strategy = greeting_factory.create_greeting_strategy(greeting_type=GreetingType.BASIC)

        assert isinstance(basic_greeting_strategy, BasicGreetingStrategy)

        holiday_greeting_strategy = greeting_factory.create_greeting_strategy(greeting_type=GreetingType.HOLIDAY)

        assert isinstance(holiday_greeting_strategy, HolidayGreetingStrategy)
