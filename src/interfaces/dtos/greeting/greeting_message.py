from pydantic import BaseModel


class GreetingMessage(BaseModel):
    first_name: str
    last_name: str

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()
