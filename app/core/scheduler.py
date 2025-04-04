from threading import Thread, Event, Lock
from queue import PriorityQueue, Queue

from ..core import Message, Source, Command, GamePage
from ..utils.logger import logger
from ..utils.maafw.maafw import maafw

class Scheduler(Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = PriorityQueue()
        self.__run_ppl = maafw.run_ppl

    def run(self):
        while True:
            p, msg = self.queue.get()
            logger.debug("Scheduler %s Got %s", self, msg)
            if not isinstance(msg, Message): logger.error("Invalid message type: %s", type(msg)); continue

            

            # TODO: dispatch message and cast workers to handle
