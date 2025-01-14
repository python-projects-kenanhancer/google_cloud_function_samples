from pydantic import BaseModel, ConfigDict

from domain import GreetingLanguage, GreetingType
from infrastructure import Environment


class GreetingCliArgs(BaseModel):
    project_env: Environment = Environment.DEV

    default_name: str = "World"
    greeting_type: GreetingType = GreetingType.BASIC
    greeting_language: GreetingLanguage = GreetingLanguage.EN

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()
