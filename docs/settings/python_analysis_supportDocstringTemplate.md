# Understanding `python.analysis.supportDocstringTemplate` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a powerful language server for Python in Visual Studio Code, offering advanced features like IntelliSense, type checking, auto-imports, and more. One of the convenient features available is automatic docstring template generation through the `python.analysis.supportDocstringTemplate` setting.

This guide explains what the `python.analysis.supportDocstringTemplate` setting is, how it works, and how you can configure it to streamline your documentation workflow.

## What is `python.analysis.supportDocstringTemplate`?

The `python.analysis.supportDocstringTemplate` setting in Pylance enables automatic generation of docstring templates for functions, classes, and methods. When enabled, typing `"""` at a docstring position will automatically generate a template with parameter descriptions, return types, and other relevant sections based on the function signature.

This feature helps you:
- **Save time**: Automatically generate the structure of docstrings without manual typing
- **Maintain consistency**: Ensure all functions have properly structured documentation
- **Reduce errors**: Avoid missing parameters or sections in your documentation
- **Follow best practices**: Use standard docstring formats recognized by documentation tools

## Supported Docstring Styles

Pylance supports multiple popular docstring formats:

### Google Style (Default)

Google style is clean and easy to read. It uses sections with indented content.

**Example:**
```python
def calculate_total(price, quantity, discount=0):
    """Calculate the total price after discount.

    Args:
        price: The unit price of the item
        quantity: The number of items
        discount: The discount percentage (default: 0)

    Returns:
        The total price after applying the discount
    """
    pass
```

### NumPy Style

NumPy style uses underlined section headers and is commonly used in scientific computing.

**Example:**
```python
def calculate_total(price, quantity, discount=0):
    """Calculate the total price after discount.

    Parameters
    ----------
    price : float
        The unit price of the item
    quantity : int
        The number of items
    discount : float, optional
        The discount percentage (default: 0)

    Returns
    -------
    float
        The total price after applying the discount
    """
    pass
```

### Sphinx Style

Sphinx style uses reStructuredText field lists and is widely used in Python documentation.

**Example:**
```python
def calculate_total(price, quantity, discount=0):
    """Calculate the total price after discount.

    :param price: The unit price of the item
    :param quantity: The number of items
    :param discount: The discount percentage (default: 0)
    :return: The total price after applying the discount
    """
    pass
```

## How to Use Docstring Templates

### Automatic Trigger

When `python.analysis.supportDocstringTemplate` is enabled, simply type `"""` inside a function, class, or method, and Pylance will automatically generate a template:

```python
def my_function(arg1, arg2):
    """|  # Type """ and the template appears
```

### Code Action

You can also generate a docstring template using a code action:
1. Place your cursor on the line with `"""`
2. Press `Ctrl+.` (or `Cmd+.` on Mac) to open the Quick Fix menu
3. Select "Generate Docstring"

## The `python.analysis.supportDocstringTemplate` Setting

### Accepted Values

- `true`: Enables automatic docstring template generation
- `false` (default): Disables the feature

### Default Value

- The default value is `false` in `default` language server mode
- The default value is `true` in `full` language server mode

## How to Change the Setting

To enable docstring template generation:

### Using Settings UI

1. Open **Settings** (File > Preferences > Settings)
2. Search for `python.analysis.supportDocstringTemplate`
3. Check the box to enable the feature

### Using settings.json

1. Open **Command Palette** (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac)
2. Type `Preferences: Open Settings (JSON)` and select it
3. Add the following line:
   ```json
   "python.analysis.supportDocstringTemplate": true
   ```

## Choosing Your Docstring Style

Pylance automatically detects and uses the appropriate docstring style based on your project's existing patterns. If no existing pattern is detected, it defaults to Google style.

**Note:** While Pylance generates the template structure, you should customize the descriptions to accurately document your code's behavior.

## Examples

### Function with Multiple Parameters

```python
def process_data(data, filters=None, normalize=True, output_format="json"):
    """Process and transform the input data.

    Args:
        data: The input data to process
        filters: Optional filters to apply (default: None)
        normalize: Whether to normalize the data (default: True)
        output_format: The desired output format (default: "json")

    Returns:
        The processed data in the specified format
    """
    pass
```

### Class with Constructor

```python
class DataProcessor:
    """A class for processing data.

    Args:
        config: Configuration dictionary
        verbose: Enable verbose logging (default: False)
    """
    
    def __init__(self, config, verbose=False):
        """Initialize the DataProcessor.

        Args:
            config: Configuration dictionary
            verbose: Enable verbose logging (default: False)
        """
        pass
```

### Function with Type Hints

When your function includes type hints, Pylance incorporates them into the generated docstring:

```python
from typing import List, Optional

def filter_items(items: List[str], pattern: Optional[str] = None) -> List[str]:
    """Filter items based on a pattern.

    Args:
        items: List of items to filter
        pattern: Optional pattern to match (default: None)

    Returns:
        Filtered list of items
    """
    pass
```

## Performance Considerations

The `python.analysis.supportDocstringTemplate` setting has minimal impact on performance since template generation only occurs when you type `"""` at a docstring position. It does not affect general IntelliSense or type checking performance.

## Frequently Asked Questions

### Q: Can I customize the docstring template format?

**A:** The template format is determined by Pylance's built-in support for standard docstring styles. For advanced customization, you may want to use the [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension alongside Pylance.

### Q: Does this work with existing docstrings?

**A:** The template generation feature is designed for creating new docstrings. It will not modify or reformat existing docstrings.

### Q: Can I trigger template generation after typing """?

**A:** Yes, you can use the code action (Quick Fix) menu after typing `"""` to generate or regenerate the template.

### Q: Does this feature work in Jupyter Notebooks?

**A:** Yes, docstring template generation works in Jupyter Notebooks when using Pylance as your language server.

### Q: What if my function signature changes?

**A:** You'll need to manually update the docstring to reflect the new signature. The template generation only occurs when you first create the docstring.

### Q: Does this replace the autoDocstring extension?

**A:** Pylance's built-in docstring template generation provides basic functionality similar to autoDocstring. However, the autoDocstring extension may offer more customization options and advanced features. You can use them together or choose the one that best fits your workflow.

## Related Settings

- **[`python.analysis.languageServerMode`](python_analysis_languageServerMode.md)**: Controls the overall feature set of Pylance. Docstring template generation is enabled by default in `full` mode.
- **`python.analysis.aiCodeActions`**: When enabled with Copilot, provides AI-assisted docstring generation for more detailed documentation.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

---

