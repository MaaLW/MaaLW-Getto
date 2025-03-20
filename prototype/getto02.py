import threading
import time
import random
from queue import PriorityQueue
import cmd
from pyreadline3 import Readline

# 用户交互界面类
class UserInterface(cmd.Cmd):
    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue
        self.prompt = ">>> "
        self.use_rawinput = False

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

# 其他子线程的任务
def worker(data_type, priority, data_queue):
    # 模拟花费一定时间收集数据
    time.sleep(random.randint(1, 5))
    
    # 收集到的数据
    data = f"Data for {data_type}"
    
    # 将数据和优先级放入队列
    data_queue.put((priority, data_type, data))

def main():
    # 创建优先级队列用于传递数据
    data_queue = PriorityQueue()
    
    readline = Readline()
    readline.parse_and_bind('tab: complete')

    # 启动用户交互界面子线程
    def run_user_interface():
        ui = UserInterface(data_queue)
        ui.cmdloop()
    
    ui_thread = threading.Thread(target=run_user_interface)
    ui_thread.start()
    
    # 创建其他子线程
    data_types = [("TypeA", 1), ("TypeB", 2), ("TypeC", 3)]
    threads = []
    
    for data_type, priority in data_types:
        thread = threading.Thread(target=worker, args=(data_type, priority, data_queue))
        thread.start()
        threads.append(thread)
    
    # 主线程持续从队列中获取数据并处理
    try:
        while True:
            # 从队列中获取数据（按优先级排序）
            priority, data_type, data = data_queue.get()
            
            # 处理数据
            print(f"Main thread received data from {data_type} (Priority {priority}): {data}")
            
            # 如果收到用户退出信号，结束主线程
            if data_type == "User" and data.lower() == "exit":
                print("Main thread exiting...")
                break
    except KeyboardInterrupt:
        print("Main thread interrupted.")
    finally:
        # 等待所有子线程完成
        for thread in threads:
            thread.join()
        ui_thread.join()

if __name__ == "__main__":
    main()