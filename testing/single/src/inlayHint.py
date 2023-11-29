# you can trigger inlay hint by opening a python file

from io import FileIO
from pathlib import Path
from typing import Optional

# confirm inlay return type
def method(a: int, b: str, /, c: Path, *, d: Optional[FileIO] = None):
    return a

# confirm inlay variable type and call arguments
var = method(10, "hello", Path("path"), d=None)
