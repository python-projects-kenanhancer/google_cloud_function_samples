import logging

from .greeting_service import GreetingService
from .greeting_strategies import BasicGreetingStrategy, HolidayGreetingStrategy, TimeBasedGreetingStrategy
from .greeting_strategy_factory import GreetingStrategyFactory
from .models import (
    GreetingLanguage,
    GreetingType,
)


class GreetingServiceFactory:

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("GreetingServiceFactory initialized with an empty registry.")

    def create(self, greeting_type: GreetingType, greeting_language: GreetingLanguage):
        """
        1) Create and configure a GreetingStrategyFactory.
        2) Create a GreetingService with the desired type/language.
        3) Return the configured service.
        """
        greeting_strategy_factory = GreetingStrategyFactory()
        greeting_strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
        greeting_strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
        greeting_strategy_factory.register(GreetingType.TIME_BASED, TimeBasedGreetingStrategy)

        greeting_service = GreetingService(
            greeting_strategy_factory=greeting_strategy_factory,
            greeting_type=greeting_type,
            greeting_language=greeting_language,
        )

        return greeting_service
