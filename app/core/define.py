from dataclasses import dataclass, field
from enum import StrEnum

from ..utils.datetime import datetime

class Command(StrEnum):
    PLAY = "play"
    STOP = "stop"
    EXIT = "exit"
    NOTIFY = "notify"
    NAVIGATE = "navigate"
    SET_VARIABLE = "set_variable"

class Source(StrEnum):
    USER = "user"
    AI = "ai"
    PLAYER = "player"
    NAVIGATOR = "navigator"
    SCHEDULER = "scheduler"

@dataclass
class Message:
    source: Source
    command: Command
    time: datetime = field(default_factory=datetime.now)
    #args: str = ""
    content: dict = field(default_factory=dict)
    pass

class GamePage(StrEnum):
    MAIN = "main"
    TITLE = "title"
    HOME = "home"
    ERRAND = "errand"
    UNKNOWN = "unknown"
    @classmethod
    def from_str(cls, s: str) -> "GamePage":
        s_lower = s.casefold()
        for member in cls:
            if member.value.casefold() == s_lower:
                return member
        return cls.UNKNOWN