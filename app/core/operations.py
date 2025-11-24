"""Compatibility module named 'operations' that re-exports calculator functions.

This file forwards functions to `calculator.py` so tests can import either name.
"""
from .calculator import add, sub, mul, div

__all__ = ["add", "sub", "mul", "div"]
