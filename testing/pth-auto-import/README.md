# `.pth` auto-import completion sample

This workspace reproduces the setup from
https://github.com/microsoft/pylance-release/issues/8225 without requiring Poetry.

1. Open this directory in VS Code using WSL.
2. Run:

   ```bash
   python3 create_environment.py
   ```

3. Select `.venv/bin/python` as the Python interpreter and reload VS Code.
4. Open `portfolio/processing/handlers/buy_handler.py`.
5. Place the cursor after `Processi` and request completions.

`ProcessingResult` should be offered with an auto-import from `.base_handler`. Typing the complete
name should also offer the quick fix `Add "from .base_handler import ProcessingResult"`.

To compare behavior without the `.pth` file, run the following command and reload VS Code:

```bash
python3 create_environment.py --remove-pth
```
