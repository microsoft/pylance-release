# you can trigger go to type definition using `Go To Type Definition` command
# use `command palette` to find the command and its short cut
# one can also use right click menu to issue the command

myVariable: int = 1


# place cursor on `myVariable` and run go to type def
# confirm it goes to the type of the expression (`int` decl in builtin), 
# not the variable `myVariable` itself (myVariable: int = 1)
print(myVariable)


class MyType:
    name: str

a = MyType()

# place cursor on `name` and run go to type def
# confirm it goes to the type of the member (`str` decl in builtin)
a.name