from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase

from ...utils.datetime import datetime


class Base(DeclarativeBase):
    pass

class Variable(Base):
    __tablename__ = "variables"

    name = Column(String(50), primary_key=True)      # 变量名（如 "level"）
    value = Column(String)                           # 变量值（JSON序列化存储）
    updated_at = Column(DateTime, default=datetime.now)  # 最近更新时间

    def __repr__(self):
        return f"<Variable(name={self.name}, value={self.value}, updated_at={self.updated_at})>"