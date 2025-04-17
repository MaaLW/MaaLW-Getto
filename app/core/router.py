# app/core/router.py
from threading import Condition
from .corethread import CoreThread, CoreExit
from .core import Message, Source, Command, GamePage
from ..utils.logger import logger
from ..utils.maafw.maafw import maafw

scheduler_commands = (Command.EXIT, Command.PLAY, Command.STOP)
varspool_commands = (Command.EXIT, Command.SET_VARIABLE,)
ai_commands = (Command.EXIT, Command.NOTIFY,)

# deprecated Use Player Instead
class Router(CoreThread):
    def __init__(self, **kwargs):
        super().__init__(process_exit_message=True, **kwargs)

    def _process(self, msg: Message, priority=100):
        if msg.command in scheduler_commands:
            self._core.scheduler.post_message(msg, priority)
        if msg.command in varspool_commands:
            self._core.varspool.post_message(msg, priority)
        if msg.command in ai_commands:
            self._core.ai.post_message(msg, priority)
        if msg.command == Command.EXIT:
            raise CoreExit(f"{self} received EXIT: {msg}")
        pass
