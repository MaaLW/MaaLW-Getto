from .player import Player, Queue, logger, CoreInterface

class GameStartPlayer(Player):
    '''
    This player would always try to go to Lostword Home Page. 
    If it fails to go home, it would stop the game and then start the game
    '''
    def __init__(
            self, 
            core: CoreInterface, 
            **kwargs
            ):
        super().__init__(core=core, **kwargs)

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