from queue import Queue
from unittest.mock import Mock
from app.core.varspool import VarsPool, VarDict
from app.core import Message, Command, Source

def test_queue_handling():
    # 初始化测试队列
    test_queue = Queue()
    vars_pool = VarsPool()
    vars_pool.queue = test_queue  # 替换为测试队列
    
    # 发送测试消息
    test_data = {"name": "sp", "value": 100}
    test_msg = Message(source=Source.USER, command=Command.SET_VARIABLE, content=test_data)
    test_queue.put(test_msg)
    
    # 处理消息
    vars_pool._handle_set_variable(test_data)
    
    # 验证结果
    assert vars_pool.get_variable("sp")["value"] == 100