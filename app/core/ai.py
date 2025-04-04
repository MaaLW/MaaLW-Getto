import threading
from queue import PriorityQueue, Queue

from ..core import Message, Source, Command
from ..utils.logger import logger

class AI(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = PriorityQueue()
        self.autopilot = False

    def run(self):
        while True:
            p, msg = self.queue.get()
            logger.debug("AI %s Got %s", self, msg)

            # TODO: dispatch message and cast workers to handle
