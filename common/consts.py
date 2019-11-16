from enum import IntEnum


class CheckerType(IntEnum):
    pass


class VerdictResult(IntEnum):
    AC = 0  # Accepted
    WA = 1  # Wrong Answer
    TLE = 1 << 1  # Time Limit Exceeded
    RE = 1 << 2  # Runtime Error
    MLE = 1 << 3  # Memory Limit Exceeded
    OLE = 1 << 4  # Output Limit Exceeded
    CE = 1 << 5  # Compile Error
    IE = 1 << 30  # Internal Error
