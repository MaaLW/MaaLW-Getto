# app/player/player.py
from threading import Thread, Event
from queue import Queue

from ..core import Message, Source, Command
from ..utils.logger import logger

class Player(Thread):

    def __init__(self, queue: Queue = None, **kwargs):
        super().__init__(**kwargs)
        self._stop_event = Event()
        self.queue = queue
        pass

    def run(self):
        '''DO NOT OVERRIDE.
        Override peri_run() instead'''
        try:
            self.pre_run()
            self.peri_run()
        finally:
            self.post_run()
        pass

    def stop(self):
        self.__set_stop()
        logger.info("%s Get Stop Signal, Will Stop Gracefully. Please Wait...", self)
        pass

    def force_stop(self):
        self.__set_stop()
        logger.info("%s Get Force Stop Signal, Will Do No More Actions and Stop Soon. Please Wait...", self)
        pass
    
    def pre_run(self):
        self.queue.put_nowait((100, Message(Source.PLAYER, Command.NOTIFY, content={"info": "start", "instance": self})))
        pass

    def post_run(self):
        self.queue.put_nowait((100, Message(Source.PLAYER, Command.NOTIFY, content={"info": "done", "instance": self})))
        pass

    def peri_run(self):
        '''
        Override this method.
        Put anything here.
        '''
        pass

    def __set_stop(self):
        self._stop_event.set()