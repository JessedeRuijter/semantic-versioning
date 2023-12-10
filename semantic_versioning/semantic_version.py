from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from functools import total_ordering
from typing import Literal

from .patterns import FULL_VERSION_PATTERN
from .utils import pad, pre_release_type_to_int

INT_TYPES = ["major", "minor", "patch", "pre_release", "post_release", "dev_release"]


@dataclass
@total_ordering
class SemanticVersion:
    """A version object."""

    major: int
    minor: int | Literal["*"] | None = None
    patch: int | Literal["*"] | None = None
    versions: list[int] = field(default_factory=list)
    pre_release_type: Literal["a", "b", "rc"] | None = None
    pre_release: int | Literal["*"] | None = None
    post_release: int | Literal["*"] | None = None
    dev_release: int | Literal["*"] | None = None

    @classmethod
    def parse(cls: type[SemanticVersion], version: str, separator: str = ".") -> SemanticVersion:
        """Initialize a Semanticversion parsed from a string.

        Attributes
        ----------
            cls (type[SemanticVersion]): the SemanticVersion class.
            version (str): the version string to parse.
            separator (str): the charachter between the major, minor and patch versions.

        Raises
        ------
            ValueError: Couldn't parse the version.

        Returns
        -------
            SemanticVersion: a SemanticVersion object.
        """
        if separator != ".":
            version.replace(separator, ".")

        if not (match := re.fullmatch(re.compile(FULL_VERSION_PATTERN), version)):
            msg = (
                f"Invalid format for semantic version {version!r}.",
                "Only X.X.X(.devX) or with other separator allowed.",
            )
            raise AssertionError(msg)

        version_dict = {}
        for k, v in match.groupdict().items():
            if not v:
                continue
            if k in INT_TYPES:
                version_dict[k] = int(v)
            elif k == "versions":
                version_dict[k] = [int(w) for w in v.split(".") if w]

        return cls(**version_dict)

    def to_string(self, separator: str = ".") -> str:
        """Convert version to a string separated with dots.

        Attributes
        ----------
            separator (str): the charachter between the major, minor and patch versions.

        Returns
        -------
            str: version string.
        """
        version = str(self.major)
        for v in [self.minor, self.patch, *self.versions]:
            if v or v == 0:
                version += f".{v}"
        if self.pre_release is not None:
            version += f"{self.pre_release_type}{self.pre_release}"
        if self.post_release is not None:
            version += f".post{self.post_release}"
        if self.dev_release is not None:
            version += f".dev{self.dev_release}"

        if separator != ".":
            version = version.replace(".", separator)
        return version

    def __str__(self) -> str:
        """Convert to string, will choose dotted version.

        Returns
        -------
            str: dot-separated version string.
        """
        return self.to_string()

    @staticmethod
    def validate(version: str) -> bool:
        """Validate if a string complies to semantic version form.

        Attributes
        ----------
            version (str): version to validate.

        Returns
        -------
            bool: if it is a valid semantic version.
        """
        pattern = re.compile(FULL_VERSION_PATTERN)
        return bool(re.fullmatch(pattern, version))

    def __eq__(self, other: SemanticVersion) -> bool:
        """Compare with another SemanticVersion if equal.

        Attributes
        ----------
            other (SemanticVersion): version to compare with.

        Returns
        -------
            bool: if the versions are equal.
        """
        return isinstance(other, SemanticVersion) and all(
            self._equal_attribute(other, attribute)
            for attribute in [*INT_TYPES, "versions", "pre_release_type"]
        )

    def _equal_attribute(self, other: SemanticVersion, attribute: str) -> bool:
        self_attribute = getattr(self, attribute)
        other_attribute = getattr(other, attribute)
        if self_attribute == "*" or other_attribute == "*":
            return True
        return self_attribute == other_attribute

    def __lt__(self, other: SemanticVersion) -> bool:
        """Compare with another SemanticVersion if smaller.

        Attributes
        ----------
            other (Any): version to compare with.

        Returns
        -------
            bool: if the version is smaller than other.
        """
        versions_length = max(len(self.versions or []), len(other.versions or []))
        return self.__compare_tuple(self, versions_length) < self.__compare_tuple(
            other,
            versions_length,
        )

    @staticmethod
    def __compare_tuple(v: SemanticVersion, v_length: int) -> tuple:
        pre_release_version = pre_release_type_to_int(v.pre_release_type)
        return (
            v.major,
            v.minor if v.minor is not None else math.inf,
            v.patch if v.patch is not None else math.inf,
            *pad(v.versions, v_length, math.inf),
            pre_release_version or math.inf if not v.post_release and not v.dev_release else -1,
            v.pre_release or math.inf if not v.post_release and not v.dev_release else -1,
            v.post_release or math.inf if not v.dev_release else -1,
            v.dev_release or math.inf,
        )

    def __hash__(self) -> int:
        """Override hash to show version dotted notation."""
        return hash(self.to_string())
