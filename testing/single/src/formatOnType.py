# you can trigger format on type by hitting enter at the end of statement

# place cursor after `:` and hit enter and confirm cursor is placed
# at the expected indentation
for a in range(10):

__break_for_statement_ # its here so that code after this is not recognized as body of the for statement.

# place cursor after `"a"` and hit enter 
ch = "a"

# place cursor after `ch:` and hit enter 
match ch:
    # place cursor after `:` and hit enter
    case "a":

__break_for_case_ # its here so that code after this is not recognized as body of the case statement.


if ch == "a":
    pass
    # type `:` after `else` and see `else` is moved to right position.
    else
    

# Set "autoFormatStrings" to true and add a { into the string below. Make sure
# it auto adds the `f` on the front. Repeat for the other strings
x = ""
y = ''
z = """""""
w = ''''''

# Make sure it doesn't add the `f` if it's already there
a = f""
b = f''
c = f"""""""
d = f''''''

# Make sure it doesn't add the `f` if it the start is a r or b string.
e = r""
f = b''
