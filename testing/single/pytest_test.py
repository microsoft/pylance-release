import pytest

# hover on `cache` and confirm fixture signature
def test_hover(cache):
    pass

# confirm `CaptureFixture[str]` is shown as inlay hint
def test_inlay_hint(capfd):
    pass

# place cursor on `pytestconfig` and run `go to defintion` and confirm
# it went to `pytestconfig` on `fixture.py`
def test_goto_definition(pytestconfig):
    pass

# place cursor on `cache` and confirm all `cache` reference is highlighted
def test_highlight_refernce(cache):
    cache.clear_cache()

# place cursor after `c` and trigger completion and confirm pytest tooltip and fixtures are listed
# see `completion.py` on how to trigger completion
def test_completion(c):
    pass