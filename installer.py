"""安装与更新逻辑：把内置文档写入项目的 conv/rules/，初始化 conv/project/ 模板。"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

from . import __version__
from .paths import LANGUAGES, bundled_doc
from .templates import project_template


def installed_dirs(project_root: Path) -> Tuple[Path, Path]:
    """返回 (rules 目录, project 目录)，均在项目根的 conv/ 下。"""
    conv_dir = project_root / "conv"
    return conv_dir / "rules", conv_dir / "project"


@dataclass
class InstallResult:
    lang: str
    version: str
    rules_path: Path
    project_path: Path
    rules_written: bool
    project_written: bool  # 仅首次创建时为 True


def _strip_reference_lines(content: str) -> str:
    """剔除指向其他 .md 文档的引用句。

    brief.md / full.md / rules.md 之间、以及指向 project/ 的交叉引用，
    只在 conventions 仓库内有效；安装后项目里只有单份文件，引用会变成死链。
    按句剔除（以 。 分句），保留同句中不含链接的内容。
    """
    lines: List[str] = []
    for raw in content.splitlines():
        if ".md)" not in raw:
            lines.append(raw)
            continue
        sentences = re.split(r"(?<=。)", raw)
        kept = "".join(s for s in sentences if ".md)" not in s).rstrip()
        if kept.strip():
            lines.append(kept)
    result = "\n".join(lines) + ("\n" if content.endswith("\n") else "")
    # 删除整行后可能留下连续空行，压缩回一个
    return re.sub(r"\n{3,}", "\n\n", result)


def _version_header(lang: str, version: str) -> str:
    """rules/ 文件顶部的版本头，标明来源。"""
    today = date.today().isoformat()
    return (
        f"<!-- conv v{__version__} | {today} | source: {lang}/{version}.md"
        f" | 由 conv 管理，执行 `conv update` 可更新。 -->\n\n"
    )


def install_language(
    project_root: Path,
    lang: str,
    version: str = "rules",
    *,
    dry_run: bool = False,
) -> InstallResult:
    """安装一门语言的规则到 project_root/conv/rules/<lang>.md。

    - 覆盖 conv/rules/<lang>.md（用户同意重复执行覆盖）
    - 若 conv/project/<lang>.md 不存在则创建模板，存在则不动
    """
    if lang not in LANGUAGES:
        raise ValueError(f"未知语言: {lang}")

    src = bundled_doc(lang, version)
    if not src.exists():
        raise FileNotFoundError(f"内置文档缺失: {src}")

    rules_dir, project_dir = installed_dirs(project_root)
    rules_path = rules_dir / f"{lang}.md"
    project_path = project_dir / f"{lang}.md"

    if not dry_run:
        rules_dir.mkdir(parents=True, exist_ok=True)
        project_dir.mkdir(parents=True, exist_ok=True)

        content = _strip_reference_lines(src.read_text(encoding="utf-8"))
        rules_path.write_text(
            _version_header(lang, version) + content, encoding="utf-8"
        )

        project_written = False
        if not project_path.exists():
            project_path.write_text(project_template(lang), encoding="utf-8")
            project_written = True
    else:
        project_written = not project_path.exists()

    return InstallResult(
        lang=lang,
        version=version,
        rules_path=rules_path,
        project_path=project_path,
        rules_written=True,
        project_written=project_written,
    )


def update_installed(
    project_root: Path,
    lang: Optional[str] = None,
    *,
    dry_run: bool = False,
) -> List[InstallResult]:
    """更新 project_root/conv/rules/ 下已装的规则。

    - 不传 lang：扫描 conv/rules/*.md，按文件名匹配内置语言逐一覆盖
    - 传 lang：只更新该语言
    - 不碰 conv/project/ 目录
    """
    rules_dir, _ = installed_dirs(project_root)
    if not rules_dir.exists():
        return []

    results: List[InstallResult] = []

    if lang is not None:
        target = rules_dir / f"{lang}.md"
        if target.exists():
            results.append(install_language(project_root, lang, "rules", dry_run=dry_run))
        return results

    for md in sorted(rules_dir.glob("*.md")):
        name = md.stem  # e.g. "python"
        if name in LANGUAGES:
            results.append(
                install_language(project_root, name, "rules", dry_run=dry_run)
            )
    return results
