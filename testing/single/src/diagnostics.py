# you can trigger diagnostics using `View: Focus Problems` 
# use `command palette` to find the command and its short cut
# but that said, it will be automatically triggered and show up as squiggles in editor
# or colored number in file explorer or entries in problems tab.

# import error
import unknownModule

# unknown identifier (semantic/checker error)
unknownIdentifier

# syntax error
:""

# type error (semantic/checker error)
# if you hover your mouse on the error, you should be able to execute code action
# associated with the error explicitly. it can be done from problem tab as well by 
# hovering icon on the entry in problem tab.
a: int = "Hello"

# unused import fading out
# these won't show up in problem tab
import os


def foo():
    # unused symbol fading out
    # these won't show up in problem tab
    a = 1


if False:
    # unreachable code fading out
    # these won't show up in problem tab
    print("unreachable code")