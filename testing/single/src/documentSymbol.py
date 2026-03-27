# SCENARIO: outline view shows the current file's symbol hierarchy
# TARGET: the current file containing `A`, its methods, `createA`, and `aInstance`
# TRIGGER: Explorer: Focus on Outline View
# EXPECT: the current editor is this file
# VERIFY: the Outline view lists the file symbols hierarchically, including class `A` with `__init__` and `getValue`, plus `createA` and `aInstance`
# RECOVER: none

# SCENARIO: outline entry selection highlights the matching symbol and double click navigates to it
# TARGET: the `getValue` entry in the Outline view for this file
# TRIGGER: single-click the Outline entry, then double-click the same entry
# EXPECT: the `getValue` symbol entry is visible in the Outline view
# VERIFY: single-click highlights the `getValue` definition in the editor and double-click navigates focus to that declaration
# RECOVER: none

# SCENARIO: go to symbol in editor exposes the editor symbol list
# TARGET: the current file containing `A`, `createA`, and `aInstance`
# TRIGGER: Go to Symbol in Editor
# EXPECT: the current editor is this file
# VERIFY: the editor-symbol picker opens and lists symbols from this file, including `A`, `createA`, and `aInstance`
# RECOVER: none
class A:
    def __init__(self, p: int):
        self.v = p

    def getValue(self) -> int:
        return self.v
    

def createA(v: int) -> A:
    return A(v)

aInstance = createA(10)