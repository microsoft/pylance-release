from zipfile import Path

from requests import ConnectTimeout


class MyType:
    def method(self, v: Path) -> ConnectTimeout:
        raise Exception("Hello")