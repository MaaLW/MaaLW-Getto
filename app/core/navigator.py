from threading import Thread, Event, Lock
from queue import PriorityQueue, Queue

from ..core import Message, Source, Command, GamePage
from ..utils.logger import logger
from ..utils.maafw.maafw import maafw

class Navigator(Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = PriorityQueue()
        self.__run_ppl = maafw.run_ppl

    def run(self):
        while True:
            p, msg = self.queue.get()
            logger.debug("Navigator %s Got %s", self, msg)
            if not isinstance(msg, Message): logger.error("Invalid message type: %s", type(msg)); continue
            if not msg.command in (Command.EXIT, Command.NAVIGATE,): logger.error("Invalid message command: %s", msg.command); continue
            if msg.command is Command.EXIT: logger.info("Navigator exiting..."); break
            #if msg.command is Command.NAVIGATE:
            logger.info("Navigator %s Got %s", self, msg)
            if (dest := GamePage.from_str(msg.content.get("dest"))) is GamePage.UNKNOWN: logger.error("Invalid dest"); continue
            if dest is GamePage.HOME:
                b, job =self.__run_ppl("Home_Go_Back_Home_Ruthlessly_v2", timeout=60)
                pass

            

            # TODO: dispatch message and cast workers to handle
