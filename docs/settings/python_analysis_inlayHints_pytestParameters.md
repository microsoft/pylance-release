# Understanding `python.analysis.inlayHints.pytestParameters` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and inlay hints that help you understand your code at a glance.

The `python.analysis.inlayHints.pytestParameters` setting controls whether Pylance displays inferred types for pytest fixture parameters in test functions.

## What `python.analysis.inlayHints.pytestParameters` does

When enabled, Pylance shows the inferred type of each pytest fixture parameter directly in the test function signature. This helps you understand what type each fixture provides without navigating to its definition.

The default value is `false`.

```json
"python.analysis.inlayHints.pytestParameters": false
```

### Example

Consider the following code:

```python
import pytest

@pytest.fixture
def my_fixture():
    return "some data"

def test_something(my_fixture):
    assert my_fixture == "some data"
```

Without inlay hints, it is not immediately clear what type `my_fixture` holds. With `python.analysis.inlayHints.pytestParameters` set to `true`, Pylance displays:

```python
def test_something(my_fixture: str):
    assert my_fixture == "some data"
```

The hint (`: str`) appears inline, showing the inferred fixture type at a glance.

### Example with a complex fixture

```python
import pytest

@pytest.fixture
def db_connection():
    return create_db_connection()

def test_query(db_connection):
    result = db_connection.execute("SELECT * FROM users")
    assert result is not None
```

With the setting enabled, Pylance displays the inferred type:

```python
def test_query(db_connection: DatabaseConnection):
    result = db_connection.execute("SELECT * FROM users")
    assert result is not None
```

## Accepted values

- `true`: Enables inlay hints for pytest fixture parameters.
- `false` (default): Disables inlay hints for pytest fixture parameters.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.inlayHints.pytestParameters`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.inlayHints.pytestParameters": true
    ```

## Prerequisites

For pytest parameter inlay hints to work, the following must be true:

- **`python.analysis.enablePytestSupport`** must be set to `true` (the default). This enables Pylance's pytest-specific features, including fixture resolution.
- Fixtures must be defined using the `@pytest.fixture` decorator.
- Test files should follow standard pytest naming conventions (`test_*.py` or `*_test.py`), and shared fixtures should be placed in `conftest.py`.

## Limitations

- **Inferred types**: Pylance infers types based on fixture return values. If a fixture returns a complex or dynamically typed value, the inferred type may be `Any` or less precise.
- **Performance**: In large codebases with many fixtures, generating these hints requires additional analysis. If you notice slowdowns, consider disabling the feature.

## Related settings

- `python.analysis.enablePytestSupport`
    - Enables or disables pytest support in Pylance, including fixture resolution and go-to-definition for fixtures. Default is `true`.
- [`python.analysis.inlayHints.variableTypes`](python_analysis_inlayHints_variableTypes.md)
    - Shows inferred types of variables.
- [`python.analysis.inlayHints.functionReturnTypes`](python_analysis_inlayHints_functionReturnTypes.md)
    - Shows return types of functions.
- [`python.analysis.inlayHints.callArgumentNames`](python_analysis_inlayHints_callArgumentNames.md)
    - Shows parameter names at call sites.

## Frequently asked questions

### Q: Inlay hints are not showing for pytest parameters. What should I check?

**A:** Verify the following:

- `python.analysis.enablePytestSupport` is set to `true`.
- Your fixtures use the `@pytest.fixture` decorator.
- Your test files follow standard pytest naming conventions (`test_*.py` or `*_test.py`).
- Shared fixtures are in `conftest.py`.
- You are using the latest version of Pylance.

### Q: Will enabling this feature affect performance?

**A:** Enabling pytest parameter inlay hints may have a slight impact on performance in large codebases, as Pylance needs to analyze fixtures to determine their types. If you experience slowdowns, you can disable the feature.

### Q: Do inlay hints modify my source code?

**A:** No. Inlay hints are visual annotations in the editor. They do not alter your source files.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._
