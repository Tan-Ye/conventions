"""project/ 目录下的模板内容（首次安装时生成，用户后续自行维护）。"""
from __future__ import annotations

from datetime import date

# 每种语言对应 project 模板里的引导文案
_PROJECT_HINTS = {
    "python": (
        "- 例：本项目数据库行统一使用 `sqlite3.Row`，不做 dict 转换\n"
        "- 例：接口层返回值统一包裹 `Result[T]`\n"
    ),
    "sql": (
        "- 例：本项目所有表必须带 `created_at` / `updated_at` 两列\n"
        "- 例：金额列名统一后缀 `_cents`\n"
    ),
    "frontend-structure": (
        "- 例：本项目页面组件统一放在 `pages/<module>/` 下\n"
        "- 例：service 层的请求拦截器统一在 `services/http.ts` 配置\n"
    ),
    "frontend-style": (
        "- 例：本项目主色为 `#1677ff`，在 `styles/global.scss` 的 `:root` 中声明\n"
        "- 例：表格行高固定 48px\n"
    ),
}


def project_template(lang: str) -> str:
    """生成 project/<lang>.md 的模板内容。"""
    hint = _PROJECT_HINTS.get(lang, "- 在此添加本项目特有的规则\n")
    today = date.today().isoformat()
    return (
        f"# 项目特有规则 · {lang}\n\n"
        f"通用规则见 [../rules/{lang}.md](../rules/{lang}.md)。\n\n"
        f"本文件只写**本项目独有**的补充规则，不重复通用规则。\n"
        f"由 `conv` 于 {today} 初始化，后续由项目维护者自行编辑。\n\n"
        f"## 在此添加\n\n"
        f"{hint}"
    )
