from pydantic import BaseModel


class GreetingRequest(BaseModel):
    first_name: str
    last_name: str

    @classmethod
    def from_dict(cls, data: dict):
        # The typed decorator will call this to parse incoming JSON
        return cls.model_validate(data)


class GreetingResponse(BaseModel):
    message: str

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()


class PersonName(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


__all__ = ["GreetingRequest", "GreetingResponse", "PersonName"]
