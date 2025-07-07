# app/core/core.py
from abc import ABC, abstractmethod

from .define import Command, Source, Message, GamePage, NotifyInfo
from .scheduler import Scheduler
from .router import Router
from .ai import AI
from .varspool import VarsPool, VarDict

class CoreInterface(ABC): # For Player to use
    @abstractmethod
    def post_message(self, msg: Message, priority=100):
        pass

    @abstractmethod
    def need_scrape(self, gp: GamePage) -> bool:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass

class Core(CoreInterface):
    def __init__(self):
        self.varspool = VarsPool()
        self.router = Router(core=self)
        self.scheduler = Scheduler()
        self.ai = AI(core=self)
    
    def start(self):
        self.varspool.start()
        self.router.start()
        self.scheduler.start()
        self.ai.start()

    def post_message(self, msg: Message, priority=100):
        self.router.post_message(msg= msg, priority= priority)

    def need_scrape(self, gp: GamePage) -> bool:
        return self.ai.need_scrape(gp)

    def is_alive(self) -> bool:
        return self.scheduler.is_alive()
#core = Core()

class CoreDummy02(CoreInterface):
    '''
    Dummy Core for Compatibility with v0.2
    '''
    def post_message(self, msg: Message, priority=100):
        pass

    def need_scrape(self, gp: GamePage) -> bool:
        return False

    def is_alive(self) -> bool:
        import threading
        return threading.main_thread().is_alive()