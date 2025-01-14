import pytest
from flask import Flask, request

from interfaces import say_hello_basic_http


class TestSayHelloBasicHttp:
    @pytest.fixture
    def app(self):
        return Flask(__name__)

    def test_say_hello_basic_http(self, app):
        with app.test_request_context("/"):
            response = say_hello_basic_http(request)
            assert response == "Hello World!"
