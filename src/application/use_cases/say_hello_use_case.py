import logging

# Domain models and services
from domain import (
    BasicGreetingStrategy,
    GreetingService,
    GreetingStrategyFactory,
    GreetingType,
    HolidayGreetingStrategy,
    PersonName,
    TimeBasedGreetingStrategy,
)
from infrastructure import SayHelloSettings

# Application-layer DTOs
from ..dtos import GreetingAppRequest, GreetingAppResponse


class SayHelloUseCase:
    """
    Coordinates the "say hello" operation.

    Responsibilities:
    1) Convert input DTO -> domain model (PersonName).
    2) Configure domain services (GreetingService) using domain settings.
    3) Execute domain logic to produce a greeting message.
    4) Return output as a DTO (GreetingResponse).

    This layer doesn't handle HTTP or external frameworks;
    it just orchestrates domain logic using domain models/services.
    """

    def __init__(self, logger: logging.Logger, say_hello_settings: SayHelloSettings):
        self.logger = logger
        self.say_hello_settings = say_hello_settings

    def _build_greeting_service(
        self,
    ) -> GreetingService:
        # a) Create & register strategies
        strategy_factory = GreetingStrategyFactory()
        strategy_factory.register(GreetingType.BASIC, BasicGreetingStrategy)
        strategy_factory.register(GreetingType.HOLIDAY, HolidayGreetingStrategy)
        strategy_factory.register(GreetingType.TIME_BASED, TimeBasedGreetingStrategy)

        # b) Create a domain service with selected type/language
        service = GreetingService(
            greeting_strategy_factory=strategy_factory,
            greeting_type=self.say_hello_settings.greeting_type,
            greeting_language=self.say_hello_settings.greeting_language,
        )
        return service

    def execute(self, request_app: GreetingAppRequest) -> GreetingAppResponse:
        # 1) Build the domain-level GreetingService
        greeting_service = self._build_greeting_service()

        # 2) Convert request to a domain model
        person_name = PersonName.model_validate(request_app.to_dict())

        # 3) Execute domain logic
        greeting_message = greeting_service.get_greeting_message(person_name)

        # 4) Log + create a response DTO
        self.logger.info("Final greeting to user: %s", greeting_message)

        return GreetingAppResponse(message=greeting_message)
