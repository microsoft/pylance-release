# you can trigger selection range using `Expand/Shrink Selection` 
# use `command palette` to find the command and its short cut
from typing import Literal


def foo(ch: Literal["a", "b", "c"]):
    match ch:
        case "a":
            pass
        case "b":
            for i in range(10):
                # place cursor at `print` and issue `Expand Selection`
                # repeat the command and confirm the selection is expanded as expected
                print(f"{ch}{i}")
        case "c":
            pass