# you can trigger quick fix explicitly using `QuickFix` command
# use `command palette` to find the command and its short cut
# since code action usually modify code, make sure `undo` work as expected.

# place cursor on `os` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'import os'` is listed
os

# place cursor on `Path` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from pathlib import Path'` is listed
Path

# place cursor on `userModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from lib import userModule'` is listed
userModule

# place cursor on `MyType` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from lib.userModule import MyType'` is listed
MyType


# place cursor on `sys` and confirm lightbulb shows up
# and trigger quick fix and confirm `remove unused import` is listed
# execute the code action and confirm it works as expected
import sys


# place cursor on `TypeToMove` and confirm lightbulb shows up
# and trigger quick fix and confirm `move symbol` is listed
# execute the code action and confirm it works as expected
# and undo to make sure undo works as expected
class TypeToMove:
    pass


# place cursor on `outerModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add "./outsideLib" to extraPaths` is listed
# execute the code action and confirm `extraPaths` is added to `settings.json`
# Undo currently does not work: https://github.com/microsoft/pylance-release/issues/5161
import outerModule


# place cursor on `hello` and confirm lightbulb shows up
# and trigger quick fix and confirm `type ignore` entry is listed
# execute the code action and confirm it added #type: ignore
a: int = "hello"


# place cursor on `unknownModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `select a different interpreter` and
# `learn more about resolving import` entry is listed
# execute the code action and confirm it works as expected
import unknownModule


# select code between `codeToExtract` and `print(codeToExtract)` and confirm lightbulb shows up
# and trigger quick fix and confirm `extract method` is listed
# execute the code action and confirm it works as expected
# confirm it can be executed through "Refactoring..." menu as well
def function():
    codeToExtract = 1
    print(codeToExtract)


# select `1 + 2 + 3` and confirm lightbulb shows up
# and trigger quick fix and confirm `extract variable` is listed
# execute the code action and confirm it works as expected
# confirm it can be executed through "Refactoring..." menu as well
print(1 + 2 + 3)


# place curosr on `userModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `Convert to relative path` is listed
# execute the code action and confirm it works as expected
from lib.userModule import ConvertImportPath


# place curosr on `mailbox` and confirm lightbulb shows up
# and trigger quick fix and confirm `Rename "...mailbox" to "...mailbox_x"` entry is listed
# execute the code action and confirm it works as expected
# Undo currently does not work: https://github.com/microsoft/pylance-release/issues/5162
import mailbox


# place curosr on `event` and confirm lightbulb shows up
# and trigger quick fix and confirm `Create Type Stub` entry is listed
# execute the code action and confirm it works as expected
# Please note that currently it doesn't work. It's a known issue tracked at
# https://github.com/microsoft/pylance-release/issues/5188
import zope.event
