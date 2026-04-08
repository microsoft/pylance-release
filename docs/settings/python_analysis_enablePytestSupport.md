# Understanding `python.analysis.enablePytestSupport` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

[pytest](https://pytest.org/) is a popular testing framework for Python, known for its simple syntax and powerful features like fixtures. Pylance offers enhanced support for pytest, providing IntelliSense features specifically designed to improve your testing workflow.

This guide explains what the `python.analysis.enablePytestSupport` setting does, how it affects your development experience with pytest, and how you can customize Pylance to suit your preferences and project needs.

## What Is `python.analysis.enablePytestSupport`?

The `python.analysis.enablePytestSupport` setting controls whether Pylance enables specialized IntelliSense features for pytest. When enabled, Pylance provides:

- **Go to Definition for fixtures**: Navigate to the definition of a pytest fixture by clicking on its usage in test function parameters.
- **Inlay hints for fixture parameters**: Display inline type hints for pytest function parameters, improving code readability.

## The `python.analysis.enablePytestSupport` Setting

### Accepted Values

- `true` (default): Enables pytest-specific IntelliSense features.
- `false`: Disables pytest-specific IntelliSense features.

### Default Value

The default value is `true`.

In [`languageServerMode`](python_analysis_languageServerMode.md) `"light"` mode, this setting defaults to `false` to optimize for performance, unless you explicitly set it to `true`.

## How to Change the Setting

To adjust `python.analysis.enablePytestSupport`:

- Open **Settings** and search for `python.analysis.enablePytestSupport`.
- Toggle the setting on or off.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)\*\*, and select it.
- Add or update the following line:
    ```json
    "python.analysis.enablePytestSupport": false
    ```

## Features Enabled by Pytest Support

### Go to Definition for Fixtures

In pytest, fixtures are a powerful feature that allows you to define reusable setup and teardown code that can be injected into your tests. Pylance enhances fixture usage by allowing you to navigate to their definitions.

**Example**:

```python
# conftest.py
import pytest

@pytest.fixture
def my_fixture():
    return "Hello, World!"
```

```python
# test_example.py
def test_greeting(my_fixture):
    assert my_fixture == "Hello, World!"
```

With pytest support enabled, you can Ctrl+Click (or Cmd+Click on macOS) on `my_fixture` in `test_example.py` to go directly to its definition in `conftest.py`.

### Inlay Hints for Fixture Parameters

Pylance can display inlay hints for pytest function parameters, showing the inferred type of each fixture:

```python
def test_example(my_fixture):
    # Inlay hint shows: my_fixture: str
    assert isinstance(my_fixture, str)
```

Inlay hints for pytest parameters are controlled separately by the `python.analysis.inlayHints.pytestParameters` setting.

## Performance Considerations

Enabling pytest support requires Pylance to analyze fixture definitions and usages across your test code. In large codebases with extensive test suites, this can consume additional memory and CPU resources.

If you experience performance issues:

- Set `python.analysis.enablePytestSupport` to `false` to disable pytest-specific features
- Adjust [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md) to `"openFilesOnly"` to limit analysis scope
- Use [`python.analysis.exclude`](python_analysis_exclude.md) to exclude test directories you're not working on

## Frequently Asked Questions

### Q: Will disabling pytest support affect other Pylance features?

**A:** No. Disabling pytest support only turns off pytest-specific IntelliSense features (fixture go-to-definition and inlay hints). All other Pylance features — code completion, type checking, diagnostics, hover — continue to work normally.

### Q: I'm not using pytest. Should I disable this?

**A:** If your project doesn't use pytest, disabling this setting avoids unnecessary analysis overhead. Set it to `false`:

```json
"python.analysis.enablePytestSupport": false
```

### Q: Why doesn't Go to Definition work on my fixture?

**A:** Verify that:

- `python.analysis.enablePytestSupport` is `true`
- The fixture is defined using `@pytest.fixture` (not a custom decorator that wraps it)
- `pytest` is installed in the active Python environment
- Pylance has finished analyzing (check the status bar)

## Related Settings

- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md): In `"light"` mode, pytest support defaults to `false`.
- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md): Controls how many files are analyzed, affecting fixture discovery scope.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._
