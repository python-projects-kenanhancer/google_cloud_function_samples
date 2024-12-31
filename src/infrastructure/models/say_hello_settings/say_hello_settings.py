from pydantic import BaseModel

from domain import GreetingLanguage, GreetingType


class SayHelloSettings(BaseModel):
    default_name: str
    greeting_type: GreetingType
    greeting_language: GreetingLanguage
