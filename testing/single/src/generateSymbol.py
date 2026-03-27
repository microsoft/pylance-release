# ENV: reuse ../.venv
# SCENARIO: generate a simple function with Copilot code action
# TARGET: `simpleMethod` in the call below
# TRIGGER: run the `generate function` code action
# EXPECT: Copilot consent is already accepted and the selected interpreter is valid for the workspace
# VERIFY: generated code is inserted without syntax errors and without corrupting surrounding code structure
# RECOVER: undo until the file matches its original text
simpleMethod() 

# SCENARIO: generate a parameterized function with Copilot code action
# TARGET: `methodWithArguments` in the call below
# TRIGGER: run the `generate function` code action
# EXPECT: Copilot consent is already accepted and the selected interpreter is valid for the workspace
# VERIFY: generated code reflects the call shape well enough to leave syntactically valid surrounding code in place
# RECOVER: undo until the file matches its original text
methodWithArguments(10, "hello")

# SCENARIO: generate a simple class with Copilot code action
# TARGET: `SimpleClass` in the construction below
# TRIGGER: run the `generate class` code action
# EXPECT: Copilot consent is already accepted and the selected interpreter is valid for the workspace
# VERIFY: generated code inserts a syntactically valid class definition without damaging nearby code
# RECOVER: undo until the file matches its original text
c = SimpleClass()

left = 1
right = 2

# SCENARIO: generate a stateful class with Copilot code action
# TARGET: `ComplexClass` in the construction below
# TRIGGER: run the `generate class` code action
# EXPECT: Copilot consent is already accepted and the selected interpreter is valid for the workspace
# VERIFY: generated code handles the constructor shape and member access well enough to leave syntactically valid surrounding code in place
# RECOVER: undo until the file matches its original text
f = ComplexClass(left, right)

a = f.left
b = f.right
c = f.combine()