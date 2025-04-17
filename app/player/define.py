from enum import StrEnum, auto


class NavigateResult(StrEnum):
    SUCCEEDED = auto()
    FAILED = auto()
    STOPPED = auto()
    PENDING = auto()
    RUNNING = auto()