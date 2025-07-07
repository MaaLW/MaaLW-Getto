# app/player/errand_player.py
import threading

from .player import Player, Queue, logger, CoreInterface
from ..utils.datetime import datetime, timedelta, sleep
from ..utils.custom.errand import Errand

class ErrandPlayer(Player):
    def __init__(self, 
                 core: CoreInterface, 
                 **kwargs):
        super().__init__(core=core, **kwargs)
        self.retry_count = 0
    def peri_run(self):
        while not self._stop_event.is_set():
            logger.info("%s Working. Retried %s Times ...", self, self.retry_count)
            # TODO: Navigate to Errand Page
            errand_list = self.__get_errand_list()
            # TODO: RUN RECO, POST Errand List to AI, GET Instructions from AI, RUN Action, RUN RECO & POST to AI again
            # Require an AI thread to decide which Errand to choose
            # Require a new action to Start New Errand
            self.retry_count += 1
            if not threading.main_thread().is_alive():
                break
        pass

    def force_stop(self):
        super().force_stop()
        pass

    def __get_errand_list(self) -> tuple[Errand]:
        # MUST BE AT ERRAND PAGE initial state
        # On Failure returns EMPTY TUPLE
        job = self._run_ppl(entry="Common_Entrance", timeout=10)
        pass