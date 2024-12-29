import pytest

from cloud_functions.say_hello_advanced_http import GreetingRequest, GreetingResponse, say_hello_advanced_http_handler


class TestSayHelloAdvancedHttp:
    @pytest.mark.parametrize(
        "first_name, last_name, expected_message",
        [
            ("John", "Doe", "Hello John Doe!"),
            ("Alice", "Smith", "Hello Alice Smith!"),
            ("", "Nobody", "Hello  Nobody!"),
        ],
    )
    def test_say_hello_advanced_http(self, first_name, last_name, expected_message):
        request_obj = GreetingRequest(first_name=first_name, last_name=last_name)

        response_obj = say_hello_advanced_http_handler(request_obj)

        assert isinstance(response_obj, GreetingResponse)
        assert response_obj.message == expected_message
