from .player import Player, Queue, logger, CoreInterface, GamePage, NavigateResult
from ..utils.emulator import Emulator, EmulatorFactory

class EmuPlayer(Player):
    '''
    This player can manipulate emulator.

    This player would always try to go to Lostword Home Page. 
    If it fails to go home, it would stop the game and then start the game
    '''
    def __init__(
            self, 
            emulator: Emulator,
            core: CoreInterface, 
            **kwargs
            ):
        super().__init__(core=core, **kwargs)
        self._emulator = emulator

    def peri_run(self):
        # TODO: Check if game has started
        # Scene01: Game Crashed, AI would call this player
        # Scene02: Game Stuck (Failed to go Home)
        # Scene03: Restart Game (Soft)
        # Scene04: Restart Game
        # Scene05: 
        # Should handle Download Query Dialog & Wait for Downloading

        #PSEUDO CODE
        # Check for Date-Changed / Maintainance / Network-Error Force-Log-Out Dialog
        pass
    
    def _soft_restart_game(self) -> bool:
        navigation_result = self._navigate(dest=GamePage.HOME)
        if navigation_result is not NavigateResult.SUCCEEDED:
            return False
        b, job = self._run_ppl("Home_Go_Back_Title_v1", timeout=30)
        if not b or not job.succeeded:
            logger.error("%s Failed to go back to title page", self)
            return False
        b, job = self._run_ppl("Home_Enter_Home_v1_Entry", timeout=30, pipeline_override=
                               {"Home_Enter_Home_v1_Entry":{"timeout": 30000}})
        if not b or not job.succeeded:
            logger.error("%s Failed to enter home page", self)
            return False
        return True
    
    def _hard_restart_game(self) -> bool:
        if not self._is_game_stopped(): # not stopped, try to stop
            self._stop_game()
        if not self._wait_game_stopped():
            logger.error("Failed to stop game")
            return False
        self._start_game()
        if self._wait_game_ready() is False:
            logger.error("Failed to start game")
            return False
        b, job = self._run_ppl("Home_Enter_Home_v1_Entry", timeout=120, pipeline_override=
                               {"Home_Enter_Home_v1_Entry":{"timeout": 120000}})
        if not b or not job.succeeded:
            logger.error("%s Failed to enter home page", self)
            return False        
        return True
    
    def _soft_restart_emulator(self) -> bool:
        if self._is_emulator_running():
            if self._restart_emulator() is False:
                return False
        else:
            self._start_emulator()
        return self._wait_emulator_ready()
    
    def _hard_restart_emulator(self) -> bool:
        if self._is_emulator_running():
            if self._stop_emulator() is False:
                return False
        self._start_emulator()
        return self._wait_emulator_ready()

    def _is_emulator_running(self) -> bool:
        return self._emulator.is_running()
    
    def _restart_emulator(self) -> bool:
        return self._emulator.restart()

    def _start_emulator(self) -> bool:
        return self._emulator.start()
    
    def _stop_emulator(self, force: bool = False) -> bool:
        return self._emulator.stop(force=force)
    
    def _start_game(self) -> bool:
        return self._emulator.start_app()
    
    def _stop_game(self) -> bool:
        return self._emulator.stop_app()
    
    def _is_game_running(self) -> bool:
        return self._emulator.is_app_running()
    
    def _is_game_stopped(self) -> bool:
        return self._emulator.is_app_stopped()
    
    def _is_emulator_ready(self) -> bool:
        return self._emulator.is_ready()

    def _wait_emulator_ready(self, timeout: int = 300) -> bool:
        return self._emulator.wait_until_ready(timeout=timeout)
    
    def _wait_game_ready(self, timeout: int = 30) -> bool:
        return self._emulator.wait_until_app_ready(timeout=timeout)
    
    def _wait_game_stopped(self, timeout: int = 30) -> bool:
        return self._emulator.wait_until_app_stopped(timeout=timeout)
    
    def force_stop(self):
        super().force_stop()
        self._emulator = EmulatorFactory.create_emulator("dummy")