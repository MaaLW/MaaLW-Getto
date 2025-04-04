import pytest
from app.utils.datetime import datetime, timedelta
from app.core.varspool.storage import VariableStorage, VarDict
from app.core.varspool.models import Variable

@pytest.fixture
def memory_storage():
    """使用内存数据库的测试fixture"""
    return VariableStorage(db_url="sqlite:///:memory:")

def test_variable_persistence(memory_storage):
    assert isinstance(memory_storage, VariableStorage)
    # 测试插入新变量
    memory_storage.update_variable("level", 5)
    var_data = memory_storage.get_variable("level")
    assert isinstance(var_data, VarDict)
    assert var_data.get("value") == 5
    assert var_data.value == 5
    
    # 测试更新变量
    memory_storage.update_variable("level", 10)
    updated_data = memory_storage.get_variable("level")
    assert isinstance(updated_data, dict)
    assert updated_data.get("value") == 10
    
    # 验证数据库记录数
    with memory_storage._get_session() as session:
        count = session.query(Variable).count()
        assert count == 1  # 确保只有一条记录

def test_serialization(memory_storage):
    assert isinstance(memory_storage, VariableStorage)
    # 测试时间类型序列化
    test_time = datetime.now()
    memory_storage.update_variable("errand_finish_time", test_time)
    
    # 验证数据库存储格式
    with memory_storage._get_session() as session:
        var = session.query(Variable).filter_by(name="errand_finish_time").first()
        assert var.value == test_time.isoformat()
    
    # 验证反序列化
    cached_data = memory_storage.get_variable("errand_finish_time")
    assert cached_data["value"] == test_time