from pydantic import BaseModel

#
# WIDGET SCHEMAS
#


class TextParagraph(BaseModel):
    text: str


class TextParagraphWidget(BaseModel):
    text_paragraph: TextParagraph


class Image(BaseModel):
    image_url: str


class ImageWidget(BaseModel):
    image: Image


# A widget can be either a textParagraph widget or an image widget.
Widget = TextParagraphWidget | ImageWidget


class CardSection(BaseModel):
    widgets: list[Widget]


class CardHeader(BaseModel):
    title: str


class Card(BaseModel):
    name: str
    header: CardHeader
    sections: list[CardSection]


class Sender(BaseModel):
    display_name: str
    avatar_url: str


class ChatMessage(BaseModel):
    sender: Sender


# (Optional) If you want to expose only certain names from this module:
__all__ = [
    "Sender",
    "ChatMessage",
    "TextParagraph",
    "TextParagraphWidget",
    "Image",
    "ImageWidget",
    "Widget",
    "CardSection",
    "CardHeader",
    "Card",
]
