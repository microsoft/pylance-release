# you can trigger document highlight using `Trigger Symbol Highlight` 
# use `command palette` to find the command and its short cut
# but that said, it will automatically run if you put cursor on top
# of supported symbol

from typing import Literal

# place cursor on `variable` and confirm all `variable` referenced in the document
# is highlighted
variable = "Hello"

print(variable)

# place cursor on `ch` and confirm the same
for ch in variable:
    print(ch)


# place cursor on `ConstructorHR` and confirm all references are highlighted
class ConstructorHR:
    # place cursor on `__init__` and confirm all references of object creation are highlighted
    def __init__(self):
        pass

def foo(i: ConstructorHR) -> ConstructorHR:
    return ConstructorHR()
