"""Runtime checks for repro_8290_protocol_constraints (stdlib only)."""
from repro_8290_protocol_constraints import CGeneric, CInt


def test_concrete_class_shape():
    assert CInt().m(1) == 1


def test_generic_class_shape():
    assert CGeneric[int]().m(2) == 2
    assert CGeneric[str]().m("a") == "a"
