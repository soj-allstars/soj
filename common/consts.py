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
    PE = 1  # Presentation Error
    TLE = 2  # Time Limit Exceeded
    MLE = 3  # Memory Limit Exceeded
    WA = 4  # Wrong Answer
    RE = 5  # Runtime Error
    OLE = 6  # Output Limit Exceeded
    CE = 7  # Compile Error
    SE = 8  # System Error


@unique
class LanguageEnum(IntEnum):
    CPP = 1
    C = 2
    Java = 3
    Python2 = 4
    Python3 = 5
    Go = 6
    JavaScript = 7
