from pydantic import BaseModel, ConfigDict

from domain import GreetingLanguage, GreetingType

from . import DatadogSettings, Environment


class Settings(BaseModel):
    project_env: Environment = Environment.DEV

    default_name: str
    greeting_type: GreetingType
    greeting_language: GreetingLanguage
    datadog: DatadogSettings

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()
