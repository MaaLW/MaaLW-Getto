import threading
import atexit
from queue import PriorityQueue, Empty
from weakref import WeakSet

from .core import Message, Command, Source
from ..utils.logger import logger

class CoreExit(Exception):
    pass

class CoreThread(threading.Thread):
    _registry = WeakSet()  # 自动管理实例生命周期
    _registry_lock = threading.Lock()  # 线程安全访问注册表
    _exit_flag = threading.Event()  # 全局退出标志

    def __init__(self, core=None, process_exit_message=False, **kwargs):
        super().__init__(**kwargs)
        self.queue = PriorityQueue()
        self._register_instance()
        self._b_process_exit_message = process_exit_message
        from .core import Core
        self._core: Core = core

    def _register_instance(self):
        """将新实例加入注册表"""
        with CoreThread._registry_lock:
            CoreThread._registry.add(self)

    @classmethod
    def request_exit(cls):
        """设置全局退出标志并发送退出消息"""
        cls._exit_flag.set()
        with cls._registry_lock:
            for instance in cls._registry:
                try:
                    assert isinstance(instance, CoreThread)
                    # 发送最高优先级的EXIT消息
                    instance.post_message(
                        msg= Message(source=Source.CORE, command=Command.EXIT), 
                        priority= 0)
                except Exception as e:
                    logger.error(f"Failed to send EXIT to {instance}: {e}")

    def run(self):
        try:
            self._pre_loop()
            self._msgloop()
        finally:
            self._post_loop()

    def _pre_loop(self):
        logger.info("Starting Core Thread %s...", self)

    def _post_loop(self):
        logger.info("Exiting Core Thread %s...", self)

    def _msgloop(self):
        while not CoreThread._exit_flag.is_set():  # 双重退出检查
            try:
                # 带超时的get避免永久阻塞
                priority, msg = self.queue.get(timeout=30)
                assert isinstance(msg, Message)
                logger.debug("%s Got %s", self, msg)
                if not self._b_process_exit_message and msg.command is Command.EXIT:
                    break
                self._process(msg, priority)
            except Empty:
                continue  # 超时后重新检查退出标志
            except CoreExit as e: # For CoreThreads who process EXIT, raise CoreException to quit msgloop
                logger.info(e)
                break
            except Exception as e:
                logger.error(e)

    def _process(self, msg: Message, priority=100):
        pass

    def post_message(self, msg: Message, priority=100):
        self.queue.put_nowait((priority, msg))

# 注册程序退出时的清理逻辑
atexit.register(CoreThread.request_exit)