from injector import inject, singleton

from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import LoggerStrategy
from interfaces.dtos import GreetingCliArgs


@singleton
class GreetingCommand:
    @inject
    def __init__(
        self,
        say_hello_use_case: SayHelloUseCase,
        logger: LoggerStrategy,
    ):
        self._say_hello_use_case = say_hello_use_case
        self._logger = logger

    def execute(self, first_name: str, last_name: str, args: GreetingCliArgs) -> None:
        # Map CLI args to application DTO
        request_app = GreetingAppRequest(first_name=first_name, last_name=last_name)

        # Execute use case
        response = self._say_hello_use_case.execute(request_app)

        # Output response
        self._logger.info(response.message)
