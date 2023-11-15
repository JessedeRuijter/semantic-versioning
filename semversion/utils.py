import math
from typing import Any, Literal


def pre_release_type_to_int(pre_release_type: Literal["a", "b", "rc"] | None) -> int:
    if not pre_release_type:
        return math.inf
    types = {
        "a": 0,
        "b": 1,
        "rc": 2,
    }
    return types[pre_release_type]


def pad(versions: list, length: int, pad_item: Any) -> list:
    pad_length = length - len(versions)
    return versions + [pad_item] * pad_length
