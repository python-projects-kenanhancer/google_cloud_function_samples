from pydantic import BaseModel, ConfigDict

from . import ChatMessage


class ChatHttpRequest(BaseModel):
    message: ChatMessage

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()

    @classmethod
    def from_dict(cls, req: dict):
        """
            If you want to keep a similar interface to your dataclass version,
            you can implement a .from_dict() method that leverages Pydantic's
        .model_validate under the hood.
        """
        return cls.model_validate(req)
