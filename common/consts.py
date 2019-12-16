from enum import IntEnum, unique


@unique
class CheckerType(IntEnum):
    same = 0
    acmp = 1
    caseicmp = 2
    casencmp = 3
    casewcmp = 4
    dcmp = 5
    fcmp = 6
    hcmp = 7
    icmp = 8
    lcmp = 9
    ncmp = 10
    nyesno = 11
    pointscmp = 12
    rcmp = 13
    rcmp4 = 14
    rcmp6 = 15
    rcmp9 = 16
    rncmp = 17
    uncmp = 18
    wcmp = 19
    yesno = 20
    special_judge = 100


@unique
class VerdictResult(IntEnum):
    AC = 0  # Accepted
    WA = 1  # Wrong Answer
    TLE = 1 << 1  # Time Limit Exceeded
    RE = 1 << 2  # Runtime Error
    MLE = 1 << 3  # Memory Limit Exceeded
    OLE = 1 << 4  # Output Limit Exceeded
    CE = 1 << 5  # Compile Error
    IE = 1 << 30  # Internal Error


@unique
class LanguageEnum(IntEnum):
    CPP = 1
    C = 2
    Java = 3
    Python2 = 4
    Python3 = 5
    Go = 6
    JavaScript = 7
