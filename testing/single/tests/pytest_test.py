import pytest

# hover on `cache` and confirm fixture signature
def test_hover(cache):
    pass

# confirm `CaptureFixture[str]` is shown as inlay hint
def test_inlay_hint(capfd):
    pass

# double click `LogCaptureFixture` and confirm the type is injected
def test_inlay_hint_type_injection(caplog):
    pass

# place cursor on `pytestconfig` and run `go to defintion` and confirm
# it went to `pytestconfig` on `fixture.py`
def test_goto_definition(pytestconfig):
    pass

# place cursor on `cache` and confirm all `cache` reference is highlighted
# including one in `test_hover`
def test_highlight_refernce(cache):
    cache.clear_cache()

# place cursor after `c` and trigger completion and confirm pytest tooltip and fixtures are listed
# see `completion.py` on how to trigger completion
def test_parameter_completion(c):
    pass

# place cursor after `capfdbinary.` and trigger completion and 
# confirm CaptureFixture[bytes]'s members are listed
def test_fixture_completion(capfdbinary):
    capfdbinary.

# hover `close` and confirm tooltip for close is provided.
def test_fixture_hover(capfdbinary):
    capfdbinary.close

# place cursor inside of `()` at `genitems()` and trigger signature help
# and confirm the signature help
def test_fixture_signatureHelp(pytester):
    pytester.genitems()

# place cursor at `clear` and trigger go to definition
def test_fixture_gotodef(doctest_namespace):
    doctest_namespace.clear()

# place cursor on `pytester` and confirm light bulb shows up with `Add type annotation ...` entry
# select pytest code actions and confirm correct imports are added
def test_fixture_codeAction(pytester):
    pass
