# app/player/errand_player.py
import threading
from time import sleep

from app.player.player import Player
from ..utils.logger import logger
from ..utils.datetime import datetime, timedelta
from ..utils.maafw import Tasker

class ErrandPlayer(Player):
    def __init__(
            self, *,
            tasker: Tasker
            ):
        threading.Thread.__init__(self)
        self.tasker = tasker
        self.b_stop = False