# Use `Go to Symbol in Workspace` from the command palette or its shortcut.
from typing import TypedDict


# SCENARIO: find the TypedDict symbol by exact name
# TARGET: query text `MyDict`
# TRIGGER: run `Go to Symbol in Workspace` and enter `MyDict`
# EXPECT: the picker shows a `MyDict` result from this file
# VERIFY: selecting the `MyDict` result opens this file and lands on `class MyDict(TypedDict):`
# RECOVER: close the picker or navigate back if selection moved the cursor
class MyDict(TypedDict):
    pass

# SCENARIO: find the module variable by partial query
# TARGET: query text `var`
# TRIGGER: run `Go to Symbol in Workspace` and enter `var`
# EXPECT: the picker shows the module variable `var` from this file
# VERIFY: selecting the `var` result opens this file and lands on the `var = 1` line
# RECOVER: close the picker or navigate back if selection moved the cursor
var = 1


# SCENARIO: find the function symbol by query text
# TARGET: query text `foo`
# TRIGGER: run `Go to Symbol in Workspace` and enter `foo`
# EXPECT: the picker shows the function symbol `foo` from this file
# VERIFY: selecting the `foo` result opens this file and lands on `def foo():`
# RECOVER: close the picker or navigate back if selection moved the cursor
def foo():
    pass