from typing import Literal

# SCENARIO: highlight all references to a local variable
# TARGET: `variable` in the assignment below
# TRIGGER: Trigger Symbol Highlight
# EXPECT: the cursor is on `variable` in `variable = "Hello"`
# VERIFY: document highlights cover the assignment, `print(variable)`, and the `for ch in variable:` reference as the same symbol
variable = "Hello"

print(variable)

# SCENARIO: highlight all references to a loop variable
# TARGET: `ch` in the loop below
# TRIGGER: Trigger Symbol Highlight
# EXPECT: the cursor is on `ch` in `for ch in variable:`
# VERIFY: document highlights cover both the loop binding and `print(ch)` as the same symbol
for ch in variable:
    print(ch)


# SCENARIO: highlight all references to a class symbol within the file
# TARGET: `ConstructorHR` in the class definition below
# TRIGGER: Trigger Symbol Highlight
# EXPECT: the cursor is on `ConstructorHR` in `class ConstructorHR:`
# VERIFY: document highlights cover the class definition, both type annotations in `foo`, and the `ConstructorHR()` construction
class ConstructorHR:
    # SCENARIO: highlight constructor references through object creation
    # TARGET: `__init__` in the method definition below
    # TRIGGER: Trigger Symbol Highlight
    # EXPECT: the cursor is on `__init__` in `def __init__(self):`
    # VERIFY: document highlights include the `ConstructorHR()` object creation in `return ConstructorHR()` as the constructor reference
    def __init__(self):
        pass

def foo(i: ConstructorHR) -> ConstructorHR:
    return ConstructorHR()
