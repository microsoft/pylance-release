myVariable: int = 1


# SCENARIO: go to type definition on a variable resolves to its builtin type
# TARGET: `myVariable` in the print call below
# TRIGGER: Go To Type Definition
# EXPECT: the cursor is on the variable reference in `print(myVariable)`
# VERIFY: navigation opens the builtin `int` declaration rather than the local `myVariable: int = 1` assignment
print(myVariable)


class MyType:
    name: str

a = MyType()

# SCENARIO: go to type definition on a member resolves to the member type
# TARGET: `name` in `a.name`
# TRIGGER: Go To Type Definition
# EXPECT: the cursor is on the member access in the final line below
# VERIFY: navigation opens the builtin `str` declaration for the member type
a.name