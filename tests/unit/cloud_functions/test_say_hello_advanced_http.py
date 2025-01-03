import pytest

from cloud_functions import GreetingHttpRequest, GreetingHttpResponse, say_hello_advanced_http


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
        request_obj = GreetingHttpRequest(first_name=first_name, last_name=last_name)

        response_obj: GreetingHttpResponse = say_hello_advanced_http(request_obj)

        assert isinstance(response_obj, GreetingHttpResponse)
        assert response_obj.message == expected_message
