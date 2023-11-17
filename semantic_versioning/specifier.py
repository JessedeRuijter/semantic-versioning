from __future__ import annotations

import re
from dataclasses import dataclass

from .flags import Operator
from .patterns import EXPRESSION_PATTERN
from .semantic_version import SemanticVersion


@dataclass
class Expression:
    operator: Operator
    version: SemanticVersion

    @classmethod
    def parse(cls, expression: str) -> Expression:
        if match := re.fullmatch(EXPRESSION_PATTERN, expression):
            operator = Operator(match.group("operator"))
            version = int(match.group("version"))
            return cls(operator, version)
        raise ValueError(f"Couldn't match {EXPRESSION_PATTERN!r} to expression.")

    def complies(self, version: SemanticVersion) -> bool:
        match self.operator:
            case Operator.EQ:
                return version == self.version
            case Operator.NE:
                return version != self.version
            case Operator.LT:
                return version < self.version
            case Operator.LE:
                return version <= self.version
            case Operator.GT:
                return version > self.version
            case Operator.GE:
                return version >= self.version


@dataclass
class Specifier:
    expressions: list[Expression]

    @classmethod
    def parse(cls, specifier: str) -> Specifier:
        expressions = specifier.split(",")
        cls([Expression.parse(expression) for expression in expressions])

    def complies(self, version: SemanticVersion) -> bool:
        for expression in self.expressions:
            if not expression.complies(version):
                return False
        return True
