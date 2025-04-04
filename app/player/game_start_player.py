

from .player import Player, Queue, logger
from .utils.run_ppl import maafw_run_ppl, dummy_run_ppl
from ..utils.maafw import Tasker

class GameStartPlayer(Player):
    def __init__(
            self, *,
            queue: Queue,
            tasker: Tasker,
            ):
        super().__init__(queue=queue, name="ErrandPlayer")
        self.tasker = tasker
        self.__run_ppl = maafw_run_ppl

    def peri_run(self):
        # TODO: Check if game has started
        # Scene01: Game Crashed, AI would call this player
        # Scene02: Game Stuck (Failed to go Home)
        # Scene03: Restart Game (Soft)
        # Scene04: Restart Game
        # Scene05: 
        pass