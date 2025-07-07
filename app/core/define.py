from dataclasses import dataclass, field
from enum import StrEnum, auto

from ..utils.datetime import datetime
from ..utils.logger import logger

class CoreStrEnum(StrEnum):
    @classmethod
    def from_str(cls, s: str) -> StrEnum | None:
        s_lower = s.casefold()
        for member in cls:
            if member.value.casefold() == s_lower:
                return member
        return None

class Command(CoreStrEnum):
    PLAY = "play"
    STOP = "stop"
    EXIT = "exit"
    NOTIFY = "notify"
    NAVIGATE = "navigate"
    SET_VARIABLE = "set_variable"

class Source(CoreStrEnum):
    USER = "user"
    CORE = "core"
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
    def __lt__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return self.time < other.time
    pass

class GamePage(CoreStrEnum):
    MAIN = "main"
    TITLE = "title"
    HOME = "home"
    ERRAND = "errand"
    UNKNOWN = "unknown"

class NotifyInfo(CoreStrEnum):
    STARTED = auto()
    DONE = auto()
    FAILED = auto()
    SCRAPED = auto()