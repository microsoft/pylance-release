"""Repro for pylance-release#8290: TypeError in type evaluation -> protocol assignment -> type constraints."""
"""This file exercises the protocol-assignment path with constrained
TypeVars. It uses only the standard library so it runs on the original
code. A crash in Pylance telemetry (TypeError while solving type
constraints during protocol compatibility) was observed without a
repro; these cases cover the most likely shapes: value-constrained
TypeVars, bound TypeVars, and unconstrained TypeVars assigned to
constrained protocol slots.
"""
from typing import Generic, Protocol, TypeVar

T_constrained = TypeVar("T_constrained", int, str)
T_bound = TypeVar("T_bound", bound=int)
T_free = TypeVar("T_free")


class PConstrained(Protocol[T_constrained]):
    def m(self, x: T_constrained) -> T_constrained: ...


class PBound(Protocol[T_bound]):
    def m(self, x: T_bound) -> T_bound: ...


class CInt:
    def m(self, x: int) -> int:
        return x


class CGeneric(Generic[T_constrained]):
    def m(self, x: T_constrained) -> T_constrained:
        return x


def takes_int_proto(p: PConstrained) -> None:
    pass


takes_int_proto(CInt())
takes_int_proto(CGeneric[int]())
