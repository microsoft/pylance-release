# test copilot generate symbol feature
#
# * NOTE *
# 1. The very first time, vscode will ask consent to use copilot unless you already did it, 
#    it only works if that is accepted.
# 2. Make sure `interpreter` is selected, otherwise, it won't work.
#
# * What to test *
# Since it is using copilot, rather than legacy imperative implementation, 
# outcome is not deterministic. so one can't check the exact same result from the same input. 
# but the benefit is, copilot is very flexible and can handle a lot more variations.
# 
# Try some variations of the following examples and check it generates acceptable code 
# such as no syntax errors, not messing up existing code and etc
#
# * Perf *
# It uses `o1-mini` model and perf is up to `vscode`. so what it takes is what it takes.

# put caret on `simpleMethod` and run `generate function` code action
simpleMethod() 

# put caret on `methodWithArguments` and run `generate function` code action
methodWithArguments(10, "hello")

# put caret on `SimpleClass` and run `generate class` code action
c = SimpleClass()

left = 1
right = 2

# put caret on `ComplexClass` and run `generate class` code action
f = ComplexClass(left, right)

a = f.left
b = f.right
c = f.combine()