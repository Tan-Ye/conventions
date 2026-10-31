"""路径与环境检测：系统目录识别、内置文档定位。"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

# 已知语言
LANGUAGES = ("python", "sql", "frontend-structure", "frontend-style")

# CLI 语言名 → 包内文档目录（相对 package_root）
_LANG_DIRS = {
    "python": "python",
    "sql": "sql",
    "frontend-structure": "frontend/structure",
    "frontend-style": "frontend/style",
}

# 文档版本
DOC_VERSIONS = ("rules", "brief", "full")


def package_root() -> Path:
    """conv 包所在目录。"""
    return Path(__file__).resolve().parent


def data_root() -> Path:
    """内置文档根目录（即包根目录，文档直接放在 python/ sql/ frontend/ 下）。"""
    return package_root()


def bundled_doc(lang: str, version: str = "rules") -> Path:
    """返回某语言某版本的内置文档路径。"""
    if lang not in LANGUAGES:
        raise ValueError(f"未知语言: {lang}")
    if version not in DOC_VERSIONS:
        raise ValueError(f"未知版本: {version}")
    return data_root() / _LANG_DIRS[lang] / f"{version}.md"


def bundled_docs_inventory() -> List[str]:
    """列出所有内置文档的相对路径。"""
    root = data_root()
    if not root.exists():
        return []
    docs: List[str] = []
    for lang in LANGUAGES:
        d = root / _LANG_DIRS[lang]
        if d.exists():
            for p in sorted(d.glob("*.md")):
                docs.append(str(p.relative_to(root)))
    return docs


# Windows 系统目录前缀（小写比较）
_SYSTEM_DIRS_WIN = (
    r"c:\windows",
    r"c:\program files",
    r"c:\program files (x86)",
    r"c:\programdata",
)


def _normalize(p: Path) -> str:
    return str(p.resolve()).lower().replace("/", "\\")


def is_system_directory(path: Path) -> bool:
    """判断路径是否落在系统目录下（不适合装规则）。"""
    norm = _normalize(path)
    for sysdir in _SYSTEM_DIRS_WIN:
        if norm == sysdir or norm.startswith(sysdir + "\\"):
            return True
    # 也拒绝在工具自身安装目录里运行
    own = _normalize(package_root())
    if norm == own or norm.startswith(own + "\\"):
        return True
    return False


def scripts_dir() -> Path:
    """Python Scripts 目录（conv 可执行文件所在）。"""
    return Path(sys.executable).resolve().parent / "Scripts"
