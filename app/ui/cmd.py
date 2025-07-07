import cmd
from argparse import ArgumentParser

#from pyreadline3 import Readline

from app.utils.logger import logger
from app.utils.datetime import datetime
from app.core import Message, Command, Source, CoreInterface

class UserInterface(cmd.Cmd):
    def __init__(self, core:CoreInterface, prompt="Getto> "):
        super().__init__()
        self.core:CoreInterface = core
        self.prompt = prompt
        self.use_rawinput = False
        #self.readline = Readline()
        #self.readline.parse_and_bind('tab: complete')
        self.play_parser = ArgumentParser(prog="play", description="Start a player.", exit_on_error=False)
        self.play_parser.add_argument("player", type=str, help="The player to start.")
        self.play_parser.add_argument("-r", "--repeat", type=int, help="Number of repetitions")
        group = self.play_parser.add_mutually_exclusive_group()
        group.add_argument("-d", "--duration", type=lambda s: datetime.strptime(s, "%H:%M:%S") - datetime.strptime("0", "%S") + datetime.today(), dest="till", metavar="DURATION", help="Duration in HH:MM:SS format")
        group.add_argument("-t", "--till", type=lambda s: datetime.combine(datetime.today().date(), datetime.strptime(s, "%H:%M:%S").time()), help="Play Till Time in HH:MM:SS format")
        self.stop_parser = ArgumentParser(prog="stop", description="Stop current player.", exit_on_error=False)
        self.stop_parser.add_argument("-f", "--force", action="store_true", help="Force stop the player.")

    def do_fxxk(self, arg):
        """Try to send whatever you want. Can only send string in kwargs"""
        try:
            args = arg.split()
            self.core.post_message(Message(Source.USER, Command(args[0]), content={k:v for k,v in zip(args[1::2], args[2::2])}), priority=50)
        except Exception as e: 
            logger.error(e)

    def do_play(self, arg):
        """Start a player. Usage: play <player>"""
        try: args = self.play_parser.parse_args(arg.split())
        except: return
        self.core.post_message(Message(Source.USER, Command.PLAY, content=vars(args)), priority=50)

    def help_play(self):
        self.play_parser.print_help()

    def do_stop(self, arg):
        """Stop current player. Usage: stop [-f]"""
        try: args = self.stop_parser.parse_args(arg.split())
        except: return
        self.core.post_message(Message(Source.USER, Command.STOP, content=vars(args)), priority=50)

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