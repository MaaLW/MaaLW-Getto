from .player import Player
from .errand_player import ErrandPlayer
from .eternal_battle_player_v2 import EternalBattlePlayer

class PlayerFactory():
    @staticmethod
    def create_player(player_type: str, **kwargs) -> Player:
        match player_type.casefold():
            case "errand" | "errand_player":
                return ErrandPlayer(**kwargs)
            case "eternal_battle" | "eternal_battle_player" | "eternal_battle_player_v2":
                return EternalBattlePlayer(**kwargs)
            case _:
                raise NotImplementedError(f"Player type {player_type} is not implemented.")