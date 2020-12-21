import json

from pytest_socket import disable_socket
from requests import Response


def pytest_runtest_setup():
    disable_socket()


class MockResponse(Response):
    def __init__(self, content: bytes, status_code: int):
        super().__init__()
        self.encoding = "utf-8"
        self._content = content
        self.status_code = status_code


class MockSuccessResponse(MockResponse):
    def __init__(
        self,
        content=bytes(json.dumps({"message": "Success"}), "utf-8"),
        status_code=200,
    ):
        super().__init__(content, status_code)


class MockFailureResponse(MockResponse):
    def __init__(
        self,
        content=bytes(json.dumps({"message": "Failure"}), "utf-8"),
        status_code=400,
    ):
        super().__init__(content, status_code)
