from __future__ import annotations

import re
from dataclasses import dataclass

from semantic_versioning.utils import simple_eval

from .flags import Operator
from .patterns import EXPRESSION_PATTERN
from .semantic_version import SemanticVersion


@dataclass
class Expression:
    """A single expression of a specifier."""

    operator: Operator
    version: SemanticVersion

    @classmethod
    def parse(cls, expression: str) -> Expression:
        """Parse expression from a string.

        Attributes
        ----------
            expression (str): expression to parse.

        Returns
        -------
            Expression: expression as object.
        """
        if match := re.fullmatch(EXPRESSION_PATTERN, expression):
            operator = Operator(match.group("operator"))
            version = SemanticVersion.parse(match.group("version"))
            return cls(operator, version)
        msg = f"Couldn't match {EXPRESSION_PATTERN!r} to expression."
        raise ValueError(msg)

    def complies(self, version: SemanticVersion) -> bool:
        """Whether the version complies to the expression.

        Attributes
        ----------
            version (SemanticVersion): the version to compare to this expression.

        Returns
        -------
            bool: if it is compatible.
        """
        match self.operator:
            case Operator.COMPATIBLE:
                return version >= self.version and version == self.version
            case Operator.ARBITRAIR_EQ:
                raise NotImplementedError
            case _:
                return simple_eval(self.operator, version, self.version)


@dataclass
class Specifier:
    """A version specification object."""

    expressions: list[Expression]

    @classmethod
    def parse(cls, specifier: str) -> Specifier:
        """Parse specifier from a string.

        Attributes
        ----------
            specifier (str): specifier to parse.

        Returns
        -------
            Specifier: specifier as object.
        """
        expressions = specifier.split(",")
        return cls([Expression.parse(expression) for expression in expressions])

    def complies(self, version: SemanticVersion) -> bool:
        """Whether the version complies to the specifier.

        Attributes
        ----------
            version (SemanticVersion): the version to compare to this specifier.

        Returns
        -------
            bool: if it is compatible.
        """
        return all(expression.complies(version) for expression in self.expressions)
