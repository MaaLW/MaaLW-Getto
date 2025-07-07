# tests/conftest.py
import sys
from pathlib import Path

# 获取项目根目录的绝对路径（假设 tests/ 在项目根目录下）
root_dir = Path(__file__).parent.parent.resolve()

# 将项目根目录添加到 sys.path
sys.path.insert(0, str(root_dir))