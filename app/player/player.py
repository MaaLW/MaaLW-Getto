# app/player/player.py

from abc import ABC, abstractmethod
from threading import Thread

class Player(Thread, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def post_stop(self):
        pass

    @abstractmethod
    def force_stop(self):
        pass