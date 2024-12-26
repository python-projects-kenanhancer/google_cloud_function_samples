import functions_framework

from schemas import (
    Card,
    CardHeader,
    CardSection,
    ChatRequest,
    ChatResponse,
    Image,
    ImageWidget,
    TextParagraph,
    TextParagraphWidget,
)


@functions_framework.typed
def google_chatbot_http(req: ChatRequest) -> ChatResponse:
    displayName = req.message.sender.displayName
    imageUrl = req.message.sender.avatarUrl

    # Build the card objects
    header = CardHeader(title=f"Hello {displayName}!")

    avatar_text_widget = TextParagraphWidget(textParagraph=TextParagraph(text="Your avatar picture: "))
    avatar_image_widget = ImageWidget(image=Image(imageUrl=imageUrl))

    section = CardSection(widgets=[avatar_text_widget, avatar_image_widget])

    card = Card(name="Avatar Card", header=header, sections=[section])

    return ChatResponse(cardId="avatarCard", card=card)
