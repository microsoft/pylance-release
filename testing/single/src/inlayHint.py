# Inlay hints should render automatically after this Python file opens.

from io import FileIO
from pathlib import Path
from typing import Optional

# SCENARIO: show inferred return type hint for a function without an annotation
# TARGET: `def method(a: int, b: str, /, c: Path, *, d: Optional[FileIO] = None):`
# TRIGGER: open this file and wait for inlay hints to render
# EXPECT: inlay hints become visible without running an extra command
# VERIFY: a return type hint for `method` is shown at the end of the function signature
# RECOVER: none
def method(a: int, b: str, /, c: Path, *, d: Optional[FileIO] = None):
    return a

# SCENARIO: show variable type and call argument inlay hints
# TARGET: `var = method(10, "hello", Path("path"), d=None)`
# TRIGGER: with this file still open, inspect the `var = method(...)` call after inlay hints render
# EXPECT: inline hints are visible on this assignment and call site
# VERIFY: a variable type hint appears for `var`, and argument name hints appear for the positional arguments in the `method(...)` call
# RECOVER: none
var = method(10, "hello", Path("path"), d=None)
