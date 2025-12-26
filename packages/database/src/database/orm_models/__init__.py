from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path

_pkg_path = Path(__file__).parent
_pkg_name = __name__

# 只导入当前目录下的 .py 模块（跳过 __init__）
for m in iter_modules([str(_pkg_path)]):
  if not m.ispkg:
    modname = m.name
    if modname.startswith("_") or modname == "base":
      continue  # 跳过_开头的文件
    import_module(f"{_pkg_name}.{modname}")
