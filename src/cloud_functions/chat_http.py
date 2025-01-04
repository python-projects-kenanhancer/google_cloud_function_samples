import functions_framework
from injector import Injector

from application import ChatAppRequest, ChatUseCase
from cloud_functions.dtos import (
    ChatHttpRequest,
    ChatHttpResponse,
)
from infrastructure import LoggerStrategy, build_di_container, inject_injector


@functions_framework.typed
@inject_injector(build_di_container())
def chat_http(request: ChatHttpRequest, injector: Injector) -> ChatHttpResponse:

    logger = injector.get(LoggerStrategy)

    chat_use_case = ChatUseCase()

    request_app = ChatAppRequest.model_validate(request.to_dict())

    chat_message = chat_use_case.execute(request_app)

    logger.info(chat_message.model_dump_json())

    return ChatHttpResponse.model_validate(chat_message.to_dict())
