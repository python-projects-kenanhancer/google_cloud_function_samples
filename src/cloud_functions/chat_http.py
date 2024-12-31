import functions_framework

from application import ChatAppRequest, ChatUseCase
from cloud_functions.dtos import (
    ChatHttpRequest,
    ChatHttpResponse,
)


@functions_framework.typed
def chat_http(request: ChatHttpRequest) -> ChatHttpResponse:

    chat_use_case = ChatUseCase()

    request_app = ChatAppRequest.model_validate(request.to_dict())

    chat_message = chat_use_case.execute(request_app)

    return ChatHttpResponse.model_validate(chat_message.to_dict())
