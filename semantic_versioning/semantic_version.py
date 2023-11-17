from __future__ import annotations

import math
import re
from dataclasses import dataclass
from functools import total_ordering
from typing import Literal

from .patterns import FULL_VERSION_PATTERN
from .utils import pad, pre_release_type_to_int

INT_TYPES = ["major", "minor", "patch", "pre_release", "post_release", "dev_release"]


@dataclass
@total_ordering
class SemanticVersion:
    major: int
    minor: int | None = None
    patch: int | None = None
    versions: list[int] | None = None
    pre_release_type: Literal["a", "b", "rc"] | None = None
    pre_release: int | None = None
    post_release: int | None = None
    dev_release: int | None = None

    @classmethod
    def parse(cls: type[SemanticVersion], version: str, separator: str = ".") -> SemanticVersion:
        """Initialize a Semanticversion parsed from a string.

        Args:
            cls (type[SemanticVersion]): the SemanticVersion class.
            version (str): the version string to parse.
            separator (str): the charachter between the major, minor and patch versions.

        Raises:
            ValueError: Couldn't parse the version.

        Returns:
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
                v = int(v)
            elif k == "versions":
                v = [int(w) for w in v.split(".") if w]
            version_dict[k] = v

        return cls(**version_dict)

    @staticmethod
    def validate(version: str) -> bool:
        return bool(re.fullmatch(re.compile(FULL_VERSION_PATTERN), version))

    def to_string(self, separator=".") -> str:
        """Convert version to a string separated with dots.

        Args:
            separator (str): the charachter between the major, minor and patch versions.

        Returns:
            str: version string.
        """
        version = str(self.major)
        for v in filter(None, [self.minor, self.patch] + self.versions):
            version += f".{v}"
        for r in filter(None, [self.pre_release, self.post_release, self.dev_release]):
            version += str(r)

        if separator != ".":
            version = version.replace(".", separator)
        return version

    def __str__(self) -> str:
        """Convert to string, will choose dotted version.

        Returns:
            str: dot-separated version string.
        """
        return self.to_string()

    @staticmethod
    def validate(version: str) -> bool:
        """Validate if a string complies to semantic version form.

        Args:
            version (str): version to validate.
            separator (str): separator between the major, minor and patch versions.

        Returns:
            bool: if it is a valid semantic version.
        """
        pattern = re.compile(FULL_VERSION_PATTERN)
        return bool(re.fullmatch(pattern, version))

    def __eq__(self, other: SemanticVersion) -> bool:
        """Compare with another SemanticVersion if equal.

        Args:
            other (Any): version to compare with.

        Returns:
            bool: if the versions are equal.
        """
        return (
            isinstance(other, SemanticVersion)
            and self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.versions == other.versions
            and self.pre_release_type == other.pre_release_type
            and self.pre_release == other.pre_release
            and self.post_release == other.post_release
            and self.dev_release == other.dev_release
        )

    def __lt__(self, other: SemanticVersion) -> bool:
        """Compare with another SemanticVersion if smaller.

        Args:
            other (Any): version to compare with.

        Returns:
            bool: if the version is smaller than other.
        """
        versions_length = max(len(self.versions or []), len(other.versions or []))
        return self.__compare_tuple(self, versions_length) < self.__compare_tuple(
            other, versions_length
        )

    @staticmethod
    def __compare_tuple(v: SemanticVersion, v_length: int) -> tuple:
        ct = (
            v.major,
            v.minor or math.inf,
            v.patch or math.inf,
            *pad(v.versions, v_length, math.inf),
            pre_release_type_to_int(v.pre_release_type) or math.inf
            if not v.post_release and not v.dev_release
            else -1,
            v.pre_release or math.inf if not v.post_release and not v.dev_release else -1,
            v.post_release or math.inf if not v.dev_release else -1,
            v.dev_release or math.inf,
        )
        print(ct)
        return ct

    def __hash__(self) -> int:
        """Override hash to show version dotted notation."""
        return hash(self.to_string())
