import functions_framework
from flask import Request


@functions_framework.http
def say_hello_basic_http(request: Request):
    return "Hello World!"
