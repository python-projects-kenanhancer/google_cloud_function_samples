from pydantic import BaseModel

from config_loaders import ConfigLoader

from .greeting_language import GreetingLanguage
from .greeting_type import GreetingType


class SayHelloSettings(BaseModel):
    default_name: str
    greeting_type: GreetingType
    greeting_language: GreetingLanguage

    @classmethod
    def load(cls, config_loader: ConfigLoader) -> "SayHelloSettings":
        config = config_loader.load()
        return cls(**config)
