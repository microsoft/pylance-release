from typing import Mapping


class ClassWithMagicMethod:
    def __lt__(self, v: int) -> bool:
        return True
    def __len__(self) -> int:
        return 1
    

# SCENARIO: go to definition for an operator resolves to the implementing magic method
# TARGET: the `<` operator in the comparison below
# TRIGGER: Go To Definition
# EXPECT: the cursor is on the comparison operator in `a = ClassWithMagicMethod() < 1`
# VERIFY: navigation opens the `ClassWithMagicMethod.__lt__` definition in this file
a = ClassWithMagicMethod() < 1

# SCENARIO: go to definition on a string literal target
# TARGET: the `os` text inside the string literal below
# TRIGGER: Go To Definition
# EXPECT: the cursor is on the string literal token in `b = "os"`
# VERIFY: skip-ready because the legacy checklist names the target token but does not ground the expected destination or surface
b = "os"

# SCENARIO: go to definition for an imported typing symbol
# TARGET: `Mapping` in the annotation below
# TRIGGER: Go To Definition
# EXPECT: the cursor is on the imported `Mapping` reference in `c: Mapping`
# VERIFY: navigation leaves the annotation site and opens the definition for `Mapping`
c: Mapping

# SCENARIO: go to definition for `len` shows both builtin and magic-method targets
# TARGET: `len` in the call below
# TRIGGER: Go To Definition
# EXPECT: the cursor is on the builtin call name in `print(len(ClassWithMagicMethod()))`
# VERIFY: the navigation surface shows both `len` and `ClassWithMagicMethod.__len__` as definition targets
print(len(ClassWithMagicMethod()))
