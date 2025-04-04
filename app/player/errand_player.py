# app/player/errand_player.py
import threading
from time import sleep

from .player import Player, Queue, logger
from .utils.run_ppl import maafw_run_ppl, dummy_run_ppl
from ..utils.datetime import datetime, timedelta
from ..utils.maafw import Tasker
from ..utils.custom.errand import Errand

class ErrandPlayer(Player):
    def __init__(
            self, *,
            queue: Queue,
            tasker: Tasker,
            ):
        super().__init__(queue=queue, name="ErrandPlayer")
        self.tasker = tasker
        self.__run_ppl = maafw_run_ppl
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
        self.__run_ppl = dummy_run_ppl
        self.tasker.post_stop()
        pass

    def __get_errand_list(self) -> tuple[Errand]:
        # MUST BE AT ERRAND PAGE initial state
        # On Failure returns EMPTY TUPLE
        job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10)
        pass