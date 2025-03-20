import cmd
from queue import Queue
from pyreadline3 import Readline

class UserInterface(cmd.Cmd):
    def __init__(self, data_queue: Queue, prompt="Getto> "):
        super().__init__()
        self.data_queue = data_queue
        self.prompt = prompt
        self.use_rawinput = False
        self.readline = Readline()
        self.readline.parse_and_bind('tab: complete')

    def do_send(self, arg):
        """Send a user message. Usage: send <message>"""
        if arg:
            # 将用户输入放入队列，优先级为 0（最高优先级）
            self.data_queue.put((0, "User", arg))
        else:
            print("Error: Message cannot be empty.")

    def do_exit(self, arg):
        """Exit the user interface."""
        print("Exiting user interface...")
        # 将退出信号放入队列
        self.data_queue.put((0, "User", "exit"))
        return True
    
    def emptyline(self):
        pass