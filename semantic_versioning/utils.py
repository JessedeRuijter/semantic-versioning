from typing import Any, Literal


def pre_release_type_to_int(pre_release_type: Literal["a", "b", "rc"] | None) -> int | None:
    if not pre_release_type:
        return None
    types = {
        "a": 1,
        "b": 2,
        "rc": 3,
    }
    return types[pre_release_type]


def pad(versions: list | None, length: int, pad_item: Any) -> list:
    _versions = versions or []
    pad_length = length - len(_versions)
    return _versions + [pad_item] * pad_length
