# app/player/errand_player.py
import threading
from time import sleep

from .player import Player
from .utils.run_ppl import maafw_run_ppl, dummy_run_ppl
from ..utils.logger import logger
from ..utils.datetime import datetime, timedelta
from ..utils.maafw import Tasker

class ErrandPlayer(Player):
    def __init__(
            self, *,
            tasker: Tasker
            ):
        super().__init__()
        self.tasker = tasker
        self.__run_ppl = maafw_run_ppl
        self.retry_count = 0
    def run(self):
        while not self.b_stop:
            logger.info("%s Working. Retried %s Times ...", self, self.retry_count)
            sleep(1)
            self.retry_count += 1
            if not threading.main_thread().is_alive():
                break
        pass

    def force_stop(self):
        super().force_stop()
        self.__run_ppl = dummy_run_ppl
        self.tasker.post_stop()
        pass