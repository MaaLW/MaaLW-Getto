from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Variable, datetime

# if a variable needs persistence, add it to this list
intvars = ("level", "sp")
datetimevars = ("errand_finish_time",)
vars = intvars + datetimevars

class VarDict(dict):
    @property
    def value(self):
        return self.get("value")
    
    @property
    def updated_at(self):
        return self.get("updated_at")

class VariableStorage:
    def __init__(self, db_url="sqlite:///lostword.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.cache = {}  # 内存缓存变量值
        self.intvars = intvars
        self.datetimevars = datetimevars
        self.vars = vars

    def _get_session(self):
        return self.Session()

    def load_all(self):
        """启动时加载所有变量到缓存"""
        with self._get_session() as session:
            variables = session.query(Variable).all()
            for var in variables:
                self.cache[var.name] = VarDict(
                    value= self._deserialize(var.name, var.value),
                    updated_at= var.updated_at
                )

    def _serialize(self, name, value):
        """根据变量名序列化值"""
        if name in self.intvars:
            return str(value)
        elif name in self.datetimevars:
            assert isinstance(value, datetime)
            return value.isoformat()
        return str(value)

    def _deserialize(self, name, value_str):
        """根据变量名反序列化值"""
        if name in self.intvars:
            return int(value_str)
        elif name in self.datetimevars:
            return datetime.fromisoformat(value_str)
        return value_str

    def update_variable(self, name, value):
        """更新变量（写入数据库）"""
        updated_at = datetime.now()
        # 更新缓存
        self.cache[name] = VarDict(
            value= value,
            updated_at= updated_at
        )
        if name in self.vars:
            # 更新数据库
            with self._get_session() as session:
                var = session.query(Variable).filter_by(name=name).first()
                if not var:
                    var = Variable(name=name)
                
                var.value = self._serialize(name, value)
                var.updated_at = updated_at
                
                session.add(var)
                session.commit()
            
    
    def get_variable(self, name):
        """非阻塞读取（直接从缓存获取）"""
        return self.cache.get(name)