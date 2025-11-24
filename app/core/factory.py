"""Factory module providing operation objects for calculations."""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Operation(Protocol):
    def compute(self, a: float, b: float) -> float:  # pragma: no cover - trivial
        ...


class AddOperation:
    def compute(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation:
    def compute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation:
    def compute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation:
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b


class CalculationFactory:
    _mapping = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
    }

    def get(self, calc_type: str) -> Operation:
        try:
            cls = self._mapping[calc_type]
        except KeyError as exc:
            raise ValueError(f"unsupported calculation type: {calc_type!r}") from exc
        return cls()
