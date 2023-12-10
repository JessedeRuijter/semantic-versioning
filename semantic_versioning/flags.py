from enum import Enum


class Operator(str, Enum):
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    COMPATIBLE = "~="
    ARBITRAIR_EQ = "==="
