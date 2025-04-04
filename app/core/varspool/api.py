import threading
from queue import Queue
from .. import Message, Command
from .storage import VariableStorage, VarDict
from ...utils.logger import logger

class VarsPool(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.queue = Queue()          # 其他模块通过此队列发送消息
        self.storage = VariableStorage()
        self.storage.load_all()      # 初始化时加载已有数据

    def run(self):
        while True:
            try:
                msg: Message = self.queue.get()
                if msg.command == Command.SET_VARIABLE:
                    self._handle_set_variable(msg.content)
            except Exception as e:
                logger.error(e)
                continue

    def _handle_set_variable(self, data: VarDict[str, object]):
        """处理变量更新请求"""
        name = data["name"]
        value = data["value"]
        self.storage.update_variable(name, value)

    def get_variable(self, name: str) -> VarDict[str, object]:
        """非阻塞读取接口（直接返回缓存数据）"""
        return self.storage.get_variable(name)