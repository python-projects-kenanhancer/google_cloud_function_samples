from application.dtos import (
    Card,
    CardHeader,
    CardSection,
    ChatAppRequest,
    ChatAppResponse,
    Image,
    ImageWidget,
    TextParagraph,
    TextParagraphWidget,
)


class ChatUseCase:
    """
    Coordinates greeting a user and building a card that references their avatar.
    """

    def execute(self, req: ChatAppRequest) -> ChatAppResponse:
        display_name = req.message.sender.display_name
        image_url = req.message.sender.avatar_url

        # 1) Build a header with the user’s display name
        header = CardHeader(title=f"Hello {display_name}!")

        # 2) Build widgets (one for text, one for the avatar image)
        avatar_text_widget = TextParagraphWidget(text_paragraph=TextParagraph(text="Your avatar picture: "))
        avatar_image_widget = ImageWidget(image=Image(image_url=image_url))

        # 3) Build a card with sections
        section = CardSection(widgets=[avatar_text_widget, avatar_image_widget])
        card = Card(name="Avatar Card", header=header, sections=[section])

        # 4) Return an application-level response
        return ChatAppResponse(card_id="avatarCard", card=card)
