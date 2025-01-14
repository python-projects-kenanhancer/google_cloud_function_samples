import pytest

from interfaces import GreetingHttpRequest, GreetingHttpResponse, say_hello_advanced_http


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
        request = GreetingHttpRequest(first_name=first_name, last_name=last_name)

        response: GreetingHttpResponse = say_hello_advanced_http(request)

        assert isinstance(response, GreetingHttpResponse)
        assert response.message == expected_message
