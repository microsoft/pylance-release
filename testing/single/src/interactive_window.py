# This file is used for testing the interactive window in VS code
# You need the jupyter extension also installed to verify this code works.

# %%
# Run this cell first and verify it outputs "Hello world"
print("Hello world")
# Then expand the 'print' cell in the interactive window (double click it) and
# verify you can hover over 'print' and see the docstring. 

# %%
# Run this cell next and verify it outputs the current working directory
import os
print(os.getcwd())

# Restart the extension host and then run this cell below:
# %%
print("After restart")
# Verify you can also expand this cell and hover over the results

# Now try typing in the interactive window input box and make sure
# completions show up and you can execute code.