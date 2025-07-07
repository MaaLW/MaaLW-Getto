from .corethread import CoreThread
from .core import Message, Command
from ..utils.logger import logger
from ..utils.maafw.maafw import maafw

class Scheduler(CoreThread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process(self, msg: Message, priority=100):
        logger.debug("%s Processing %s", self, msg)
        # TODO: 根据具体调度逻辑实现消息处理
        if msg.command == Command.PLAY:
            logger.info("Scheduler starting playback...")
            # TODO: 实现播放调度逻辑