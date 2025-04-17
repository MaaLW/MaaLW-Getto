from time import sleep, time
from random import randint
import pytest
from app.core.varspool import VarsPool
from app.core import Message, Command, Source

@pytest.fixture
def vars_pool():
    """测试固件：初始化变量池并自动清理"""
    pool = VarsPool(db_url="sqlite:///test.db") 
    pool.start()
    yield pool
    # 测试结束后触发退出逻辑
    VarsPool.request_exit()
    pool.join(timeout=1)  # 等待线程退出

def test_queue_handling(vars_pool):    
    # 发送测试消息
    vp = vars_pool
    assert isinstance(vp, VarsPool)
    test_value = randint(500, 1000)
    test_data = {"name": "sp", "value": test_value}
    test_msg = Message(source=Source.USER, command=Command.SET_VARIABLE, content=test_data)
    vp.post_message(test_msg)
    time1 = time()
    
    # 验证结果
    while True:
        if vp.get_variable("sp").value == test_value:
            break
        if time() - time1 > 1:
            raise Exception("Test failed: Timeout")
    assert vp.get_variable("sp").value == test_value
