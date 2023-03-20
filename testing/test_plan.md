# Test plan

## Environment

-   OS: XXX (Windows, macOS, latest Ubuntu LTS)
-   Python
    -   Distribution: XXX (CPython, miniconda)
    -   Version: XXX (3.9, 3.10, 3.11, 3.12)
-   VS Code: XXX (Insiders)
-   Python, Jupyter && Pylance Extension: XXX (Insiders)

## Tests

### P0 Test Scenarios

#### Basic language services

-   [ ] Errors
    1. Open a new python file
    1. Type invalid python into it. Like `x2+2-3` on a single line.
    1. Verify you get a red squiggle
    1. Type valid python after that. 
    1. Make sure no squiggles happen
-   [ ] Import errors
    1. Create a brand new python environment
    1. Select the new environment in VS code.
    1. Open a new python file
    1. Add `import pandas as pd` at the top
    1. It should error on the pandas
    1. Open a terminal
    1. Activate your new environment
    1. Install pandas (`python -m pip install pandas`)
    1. Go back to the python file in VS code
    1. There should no longer be an error for importing pandas.
-   [ ] Completions
    1. Open a new python file
    1. Pick an interpreter on the bottom right
    1. Add an import for sys `import sys`
    1. Type `sys.` and verify you get completions
-   [ ] Hover
    1. Open a new python file
    1. Pick an interpreter on the bottom right if not already selected.
    1. Add an import for sys `import sys`
    1. Hover over `sys` and make sure it shows something
    1. Add a new function, like so
    ```python
    def foo():
        '''
        Doc string for foo 
        '''
        pass
    ```
    6. Hover over `foo` and make sure the hover info includes the doc string
    [ ] Goto definition
    1. Open a new python file
    1. Add an import for sys `import sys`
    1. Go to definition on the `sys` module.
    1. It should jump to the definition of sys in your python environment

#### Notebooks

-   [ ] Imports from files
    1. Open a new jupyter notebook
    1. Open a new python file
    1. Create a method in the python file
    1. In the first cell of the notebook, import the python file
    1. Verify no red squiggles show up
    1. In the same cell of the notebook, try calling the method you created. Something like so:
    ```python
    import test_file
    test_file.foo()
    ```
    7. Verify no red squiggles show up on the call to the test method.
    7. Goto definition on the method. It should jump to the python file.


### P1 Test Scenarios

-   [ ] Rename
    1. Open a new python file
    1. Create a method
    1. Call that method
    1. Hit F2 on the method call and rename it something else
    1. Verify the definition of the method changes

-   [ ] Rename across files
    1. Open a new python file
    1. Create a method
    1. Open another python file
    1. Import the method from the first file
    1. Rename the method from the second file
    1. Verify it is renamed in the original file too

-   [ ] Find all references
    1. Open a new python file
    1. Create a class in that python file with an `__init__` method.
    1. Open two other python files
    1. Import the first file in each
    1. Create a variable by constructing the class in the two other files
    1. Go back to the first file
    1. Find all references on the class
    1. Verify it finds the two creations in the other files
    1. Go back to the first file
    1. Find all references on the `__init__` function
    1. Verify it finds the same references as searching for the class name

### P2 Test Scenarios

-   [ ] Scikit learn
    1. Open VS code
    1. Pick `Python: Create Environment` command
    1. Pick `venv`
    1. After the environment is created, open a terminal and activate it.
    1. Install the scikitlearn requirements.txt into the environment

    ```
    python -m pip install -r ./testing/scikitlearn/requirements.txt
    ```

    6. Open the scikitlearn/test.py file.
    6. Try hovering over different methods and classes in the test.py file
    6. Try adding a new method that has a doc string. Something like so:

    ```python
    def newmethod():
        '''
        Method with docstring
        '''
        pass
    ```

    9. Make sure hover on the method works
    9. Try calling a method on the `model` object. Make sure completions come up when you type `.` after model
    9. Try `Go to definition` on `make_column_transformer` and other methods. Make sure you goto the source in scikit learn or the type stubs.

