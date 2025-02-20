# app/player/player.py

from abc import ABC, abstractmethod
from threading import Thread

class Player(Thread, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> bool:
        pass

    @abstractmethod
    def post_stop(self) -> bool:
        pass
