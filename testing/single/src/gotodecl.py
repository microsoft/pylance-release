from typing import Mapping

   
# SCENARIO: go to declaration for an operator lands in a stub file
# TARGET: the `==` operator in the comparison below
# TRIGGER: Go To Declaration
# EXPECT: the cursor is on the comparison operator in `a = 1 == 1`
# VERIFY: navigation opens a declaration in a `.pyi` file
# RECOVER: none
a = 1 == 1

# SCENARIO: go to declaration for a string literal lands in a stub file
# TARGET: the `os` text inside the string literal below
# TRIGGER: Go To Declaration
# EXPECT: the cursor is on the string literal token in `b = "os"`
# VERIFY: navigation opens a declaration in a `.pyi` file
# RECOVER: none
b = "os"

# SCENARIO: go to declaration for an imported typing symbol prefers the stub declaration
# TARGET: `Mapping` in the annotation below
# TRIGGER: Go To Declaration
# EXPECT: the cursor is on the imported `Mapping` reference in `c: Mapping`
# VERIFY: navigation opens the `Mapping` declaration in a `.pyi` file rather than a `.py` file
# RECOVER: none
c: Mapping