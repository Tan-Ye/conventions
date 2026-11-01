"""conv 命令行入口。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Sequence

from . import __version__
from .installer import (
    InstallResult,
    installed_dirs,
    install_language,
    update_installed,
)
from .paths import (
    LANGUAGES,
    bundled_doc,
    bundled_docs_inventory,
    data_root,
    is_system_directory,
    package_root,
    scripts_dir,
)

# 安装目标别名
ALIASES = {
    "all": list(LANGUAGES),
    "frontend": ["frontend-structure", "frontend-style"],
}


def _resolve_langs(target: str) -> List[str]:
    """把命令行的目标解析成具体语言列表。"""
    if target in ALIASES:
        return list(ALIASES[target])
    if target in LANGUAGES:
        return [target]
    raise SystemExit(
        f"未知目标: {target}\n"
        f"可用: {', '.join(LANGUAGES)}，或别名 all / frontend"
    )


def _check_cwd(cwd: Path) -> None:
    """拒绝在系统目录运行。"""
    if is_system_directory(cwd):
        raise SystemExit(
            f"当前目录不适合安装规则: {cwd}\n"
            "请在项目目录下执行 conv。"
        )


def cmd_install(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    _check_cwd(cwd)
    langs = _resolve_langs(args.target)
    version = args.version

    results: List[InstallResult] = []
    for lang in langs:
        results.append(
            install_language(cwd, lang, version, dry_run=args.dry_run)
        )

    gitignore_done = False
    for r in results:
        action = "（dry-run）" if args.dry_run else ""
        proj = "  + 新建 project 模板" if r.project_written else "  = project 已存在，未改动"
        print(
            f"[install] {r.lang} ({r.version}){action}\n"
            f"  -> conv/rules/{r.lang}.md\n{proj}"
        )
        if r.gitignore_updated and not gitignore_done:
            print("  -> .gitignore 已加入 conv/")
            gitignore_done = True
    print(f"\n完成：{len(results)} 个语言。")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    _check_cwd(cwd)

    lang = args.lang
    results = update_installed(cwd, lang, dry_run=args.dry_run)

    if not results:
        rules_dir, _ = installed_dirs(cwd)
        if not rules_dir.exists():
            print(f"未找到 rules/ 目录: {rules_dir}")
            print("先执行 `conv install <lang>` 安装规则。")
        else:
            print("rules/ 下没有可更新的已装规则。")
        return 1

    for r in results:
        action = "（dry-run）" if args.dry_run else ""
        print(f"[update] {r.lang}{action} -> conv/rules/{r.lang}.md")
    print(f"\n完成：{len(results)} 个语言已更新。")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    print("可安装语言：")
    for lang in LANGUAGES:
        print(f"  {lang}")
    print("\n别名：")
    print("  all        安装全部")
    print("  frontend   安装 frontend-structure + frontend-style")

    cwd = Path.cwd()
    rules_dir, _ = installed_dirs(cwd)
    if rules_dir.exists():
        installed = sorted(p.stem for p in rules_dir.glob("*.md"))
        if installed:
            print(f"\n当前项目已装 ({rules_dir}):")
            for name in installed:
                print(f"  {name}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    print(f"conv 版本: {__version__}")
    print(f"可执行文件: {scripts_dir() / 'conv.exe'}")
    print(f"包目录:     {package_root()}")
    print(f"内置文档:   {data_root()}")

    inv = bundled_docs_inventory()
    print(f"\n内置文档清单（共 {len(inv)} 份）：")
    for item in inv:
        print(f"  {item}")

    cwd = Path.cwd()
    rules_dir, project_dir = installed_dirs(cwd)
    if rules_dir.exists() or project_dir.exists():
        print(f"\n当前项目 ({cwd}):")
        if rules_dir.exists():
            installed = sorted(p.name for p in rules_dir.glob("*.md"))
            print(f"  conv/rules/   {len(installed)} 个文件: {', '.join(installed)}")
        if project_dir.exists():
            pfiles = sorted(p.name for p in project_dir.glob("*.md"))
            print(f"  conv/project/ {len(pfiles)} 个文件: {', '.join(pfiles)}")
    else:
        print(f"\n当前目录 ({cwd}) 尚未安装任何规则。")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    langs = _resolve_langs(args.target)
    version = args.version
    for lang in langs:
        src = bundled_doc(lang, version)
        if not src.exists():
            print(f"[show] {lang}: 内置文档缺失 {src}", file=sys.stderr)
            continue
        print(f"===== {lang} ({version}) =====")
        print(src.read_text(encoding="utf-8"))
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="conv",
        description="代码规范安装器：把通用规则装到项目的 rules/，项目特有规则放 project/。",
    )
    parser.add_argument(
        "--version", action="version", version=f"conv {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # install
    p_install = sub.add_parser("install", help="安装语言规则到 rules/")
    p_install.add_argument(
        "target",
        help="语言名（python/sql/frontend-structure/frontend-style）或别名（all/frontend）",
    )
    p_install.add_argument(
        "--rules",
        dest="version",
        action="store_const",
        const="rules",
        help="安装最简规则版（默认）",
    )
    p_install.add_argument(
        "--brief",
        dest="version",
        action="store_const",
        const="brief",
        help="安装精简版（规则+示例）",
    )
    p_install.add_argument(
        "--full",
        dest="version",
        action="store_const",
        const="full",
        help="安装完整版（规则+示例+理由）",
    )
    p_install.add_argument(
        "--dry-run", action="store_true", help="只打印将要写入的文件，不落盘"
    )
    p_install.set_defaults(version="rules", func=cmd_install)

    # update
    p_update = sub.add_parser("update", help="更新已装规则（覆盖 rules/，不动 project/）")
    p_update.add_argument("lang", nargs="?", default=None, help="只更新指定语言")
    p_update.add_argument(
        "--dry-run", action="store_true", help="只打印将要更新的文件，不落盘"
    )
    p_update.set_defaults(func=cmd_update)

    # list
    p_list = sub.add_parser("list", help="列出可安装语言及当前项目已装规则")
    p_list.set_defaults(func=cmd_list)

    # info
    p_info = sub.add_parser("info", help="显示安装路径、内置文档清单、项目已装情况")
    p_info.set_defaults(func=cmd_info)

    # show
    p_show = sub.add_parser("show", help="在终端打印内置文档（预览，不写文件）")
    p_show.add_argument("target", help="语言名或别名")
    p_show.add_argument(
        "--rules", dest="version", action="store_const", const="rules"
    )
    p_show.add_argument(
        "--brief", dest="version", action="store_const", const="brief"
    )
    p_show.add_argument(
        "--full", dest="version", action="store_const", const="full"
    )
    p_show.set_defaults(version="rules", func=cmd_show)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
