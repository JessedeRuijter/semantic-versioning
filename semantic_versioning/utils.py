from operator import eq, ge, gt, le, lt, ne
from typing import Literal, TypeVar

from semantic_versioning.flags import Operator

T = TypeVar("T")


def pre_release_type_to_int(pre_release_type: Literal["a", "b", "rc"] | None) -> int | None:
    """Ordering of the prereleases.

    Attributes
    ----------
        pre_release_type (Literal["a", "b", "rc"] | None): _description_

    Returns
    -------
        int | None: _description_
    """
    if not pre_release_type:
        return None
    types = {
        "a": 1,
        "b": 2,
        "rc": 3,
    }
    return types[pre_release_type]


def pad(versions: list[T] | None, length: int, pad_item: T) -> list[T]:
    """Pad the list at the end with a certain item.

    Attributes
    ----------
        versions (list | None): _description_
        length (int): _description_
        pad_item (object): _description_

    Returns
    -------
        list: _description_
    """
    _versions = versions or []
    pad_length = length - len(_versions)
    return _versions + [pad_item] * pad_length


def simple_eval(operator: Operator, left: T, right: T) -> T:
    """Find corresponding operator and evaluate for simple cases.

    Attributes
    ----------
        operator (Operator): _description_
        left (T): _description_
        right (T): _description_

    Returns
    -------
        T: _description_
    """
    operators = {
        Operator.EQ: eq,
        Operator.NE: ne,
        Operator.LT: lt,
        Operator.LE: le,
        Operator.GT: gt,
        Operator.GE: ge,
    }
    return operators.get(operator)(left, right)
