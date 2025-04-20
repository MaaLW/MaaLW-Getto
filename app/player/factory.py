from .player import Player
from .errand_player import ErrandPlayer

class PlayerFactory():
    @staticmethod
    def create_player(player_type: str, **kwargs) -> Player:
        match player_type.casefold():
            case "errand" | "errand_player":
                return ErrandPlayer(**kwargs)
            case _:
                raise NotImplementedError(f"Player type {player_type} is not implemented.")