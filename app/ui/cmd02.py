import cmd
from argparse import ArgumentParser

from app.utils.logger import logger
from app.utils.datetime import datetime
from app.core import Message, Command, Source, CoreInterface
from app.player import Player, PlayerFactory
from app.config import config

class UserInterface02(cmd.Cmd):
    '''
    For compatible with v0.2 and DummyCore02, do everything here rather than core
    '''
    def __init__(self, core:CoreInterface, prompt="Getto> "):
        super().__init__()
        self.core:CoreInterface = core
        self.prompt = prompt
        self.use_rawinput = False

        self.current_player: Player | None = None
        self.eternal_battle_recordfile: str = config["lostword.eternal_battle_record"].get("path")

        self.start_parser = ArgumentParser(prog="start", description="Start a player.", exit_on_error=False)
        self.start_parser.add_argument("repeat_times", type=int, nargs="?", default=9999, 
                                     help="Number of times to repeat (default: 9999)")
        self.stop_parser = ArgumentParser(prog="stop", description="Stop current player.", exit_on_error=False)
        self.stop_parser.add_argument("-f", "--force", action="store_true", help="Force stop the player.")

    def do_start(self, arg):
        """Start a player. Usage: start [repeat_times=9999]"""
        try: 
            args = self.start_parser.parse_args(arg.split())
            repeat_times: int = args.repeat_times
        except Exception as e:
            logger.error(f"Invalid start command: {e}")
            return
        try:
            if self.current_player is not None and self.current_player.is_alive():
                logger.warning("A Player %s is already running.", self.current_player)
            else:
                self.current_player = PlayerFactory.create_player("eternal_battle_player_v2", 
                                                                  core=self.core, 
                                                                  recordfile=self.eternal_battle_recordfile, 
                                                                  repeat_times=repeat_times)
                self.current_player.start()
        except Exception as e:
            logger.error(f"Failed to start Player: {e}")
            return

    def help_start(self):
        self.start_parser.print_help()

    def do_stop(self, arg):
        """Stop current player. Usage: stop [-f]"""
        try: 
            args = self.stop_parser.parse_args(arg.split())
        except Exception as e: 
            logger.error(f"Invalid stop command: {e}")
            return
        try:
            if self.current_player is None or not self.current_player.is_alive():
                logger.warning(f"No Player is running. Last Player is {self.current_player}")
            else:
                self.current_player.stop(args.force)
            return
        except Exception as e:
            logger.error(f"Failed to stop Player: {e}")
            return

    def help_stop(self):
        self.stop_parser.print_help()

    def do_exit(self, arg):
        """Exit the user interface."""
        logger.info("Exiting user interface...")
        # 将退出信号放入队列
        self.core.post_message(Message(Source.USER, Command.EXIT), priority=0)
        return True
    
    def emptyline(self):
        pass