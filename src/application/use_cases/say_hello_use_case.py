import logging

# Domain models and services
from domain import (
    GreetingServiceFactory,
    PersonName,
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

    def __init__(self, say_hello_settings: SayHelloSettings):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.say_hello_settings = say_hello_settings

    def execute(self, request_app: GreetingAppRequest) -> GreetingAppResponse:
        # 1) Build the domain-level GreetingService
        greeting_service = GreetingServiceFactory().create(
            self.say_hello_settings.greeting_type, self.say_hello_settings.greeting_language
        )

        # 2) Convert request to a domain model
        person_name = PersonName.model_validate(request_app.to_dict())

        # 3) Execute domain logic
        greeting_message = greeting_service.get_greeting_message(person_name)

        # 4) Log + create a response DTO
        self.logger.info("Final greeting to user: %s", greeting_message)

        return GreetingAppResponse(message=greeting_message)
