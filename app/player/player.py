# app/player/player.py

from abc import ABC, abstractmethod
from threading import Thread

from ..utils.logger import logger

class Player(Thread, ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.b_stop = False
        pass

    @abstractmethod
    def run(self):
        pass

    def post_stop(self):
        self.__stop()
        logger.info("%s Get Stop Signal, Will Stop Gracefully. Please Wait...", self)
        pass

    @abstractmethod
    def force_stop(self):
        self.__stop()
        logger.info("%s Get Force Stop Signal, Will Do No More Actions and Stop Soon. Please Wait...", self)
        pass

    def __stop(self):
        self.b_stop = True