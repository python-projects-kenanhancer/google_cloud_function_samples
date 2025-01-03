from injector import (
    Module,
    provider,
    singleton,
)

from domain import GreetingLanguage, GreetingType

from ..models.say_hello_settings import SayHelloSettings


class FakeSayHelloSettingsModule(Module):
    def __init__(self, default_name="World", greeting_type=GreetingType.BASIC, greeting_language=GreetingLanguage.EN):
        self.default_name = default_name
        self.greeting_type = greeting_type
        self.greeting_language = greeting_language

    @singleton
    @provider
    def provide_say_hello_settings(self) -> SayHelloSettings:
        return SayHelloSettings(
            default_name=self.default_name,
            greeting_type=self.greeting_type,
            greeting_language=self.greeting_language,
        )
