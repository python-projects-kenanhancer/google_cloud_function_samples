from typing import List, Union

from pydantic import BaseModel

#
# REQUEST SCHEMAS
#


class Sender(BaseModel):
    displayName: str
    avatarUrl: str


class ChatMessage(BaseModel):
    sender: Sender


class ChatRequest(BaseModel):
    message: ChatMessage

    @classmethod
    def from_dict(cls, req: dict) -> "ChatRequest":
        """
            If you want to keep a similar interface to your dataclass version,
            you can implement a .from_dict() method that leverages Pydantic's
        .model_validate under the hood.
        """
        return cls.model_validate(req)


#
# WIDGET SCHEMAS
#


class TextParagraph(BaseModel):
    text: str


class TextParagraphWidget(BaseModel):
    textParagraph: TextParagraph


class Image(BaseModel):
    imageUrl: str


class ImageWidget(BaseModel):
    image: Image


# A widget can be either a textParagraph widget or an image widget.
Widget = Union[TextParagraphWidget, ImageWidget]


#
# CARD SCHEMAS
#


class CardSection(BaseModel):
    widgets: List[Widget]


class CardHeader(BaseModel):
    title: str


class Card(BaseModel):
    name: str
    header: CardHeader
    sections: List[CardSection]


#
# RESPONSE SCHEMA
#


class ChatResponse(BaseModel):
    cardId: str
    card: Card

    def to_dict(self) -> dict:
        """
        Mirrors your original to_dict() method, but uses Pydantic's .dict()
        under the hood. Adjust the output shape if needed.
        """
        return {"cardsV2": self.dict()}


# (Optional) If you want to expose only certain names from this module:
__all__ = [
    "Sender",
    "ChatMessage",
    "ChatRequest",
    "TextParagraph",
    "TextParagraphWidget",
    "Image",
    "ImageWidget",
    "Widget",
    "CardSection",
    "CardHeader",
    "Card",
    "ChatResponse",
]
