# 代码规范

每门语言三份，按用途分。**规则只在自己那门语言里生效，不跨语言套用。**

| 语言 | 完整版（规则 + 示例 + 理由） | 精简版（规则 + 示例） | 最简版（只有规则） |
|---|---|---|---|
| Python | [full](python/full.md) | [brief](python/brief.md) | [rules](python/rules.md) |
| SQL | [full](sql/full.md) | [brief](sql/brief.md) | [rules](sql/rules.md) |
| 前端 · 组件与目录 | [full](frontend/structure/full.md) | [brief](frontend/structure/brief.md) | [rules](frontend/structure/rules.md) |
| 前端 · 样式 | [full](frontend/style/full.md) | [brief](frontend/style/brief.md) | [rules](frontend/style/rules.md) |

## 三份分别什么时候看

| 场景 | 看哪份 |
|---|---|
| 写代码时随手对照 | `rules.md` —— 一屏看完，只有规则 |
| Code review、找示例 | `brief.md` —— 每条规则配一个能抄的例子 |
| 讨论"为什么这么定"、新人上手 | `full.md` —— 规则 + 完整示例 + 理由和反例 |

三份内容必须同步：改一条规则，三个文件一起改。`rules.md` 是唯一权威，另外两份以它为准。

## 为什么按语言分

同一个概念在不同语言里的最佳实践是冲突的：

- Python 数据层推荐 `TypedDict`（运行时就是 dict，零转换）
- TypeScript 里对应的是 `type` / `interface`，但前端还要管组件 props、state 形状，规则完全不同
- SQL 关心的是索引、约束、事务边界，和代码风格无关

混在一个文件里，写到第三门语言时必然出现"这条到底管不管前端"的歧义。

## 新增一份的时机

一门语言出现**第一条它独有的规则**时，就给它建目录，不要往别人的文件里加"顺便也适用于 XX"的条目。

---

# conv —— 代码规范安装器

本仓库自带一个命令行工具 `conv`，把上面这些规范作为内置文档，安装到任意项目里。

## 设计：两层规则

```
项目根目录/
└── conv/
    ├── rules/              通用规则，由 conv 安装/更新，内容来自本仓库内置文档
    │   ├── python.md
    │   ├── sql.md
    │   ├── frontend-structure.md
    │   └── frontend-style.md
    └── project/            项目特有规则，用户自己维护，conv 不覆盖
        ├── python.md
        ├── sql.md
        ├── frontend-structure.md
        └── frontend-style.md
```

- `conv/rules/`：通用层。工具负责写入，等于"内置文档的本地副本"。
- `conv/project/`：项目层。写项目独有的补充规则（对应各语言 `full.md` 顶部引用的 `project/*.md`）。

## 安装

```bash
# 在本仓库根目录下执行
pip install .
```

安装后 `conv` 命令全局可用。安装位置：

| 内容 | 位置 |
|---|---|
| `conv` 可执行文件 | Python 的 `Scripts` 目录（如 `...\Python\Python3xx\Scripts\conv.exe`） |
| 工具代码 + 内置文档 | Python 的 `site-packages\conv\` |
| 内置 md 文档 | `site-packages\conv\` 下 12 份（4 语言 × 3 版本，即 `python\`、`sql\`、`frontend\` 子目录） |

> `pip install .` 会自动把 Python 的 `Scripts` 目录加入用户 PATH，**重开终端**后 `conv` 即可全局使用。

> **安装时引用行会被剔除**：仓库内的文档头部有指向兄弟文件的交叉引用（如"要示例看 brief.md，要理由看 full.md"、"项目特有约定见 project/xxx.md"）。这些链接只在 conventions 仓库内有效——安装到项目后只有单份 `conv/rules/<语言>.md`，引用会变成死链。因此 `conv install` / `conv update` 写入时会自动删除含 `.md` 链接的引用句，保留"适用范围"等无链接内容。仓库内的源文档保持原样不受影响。

## 命令

| 命令 | 说明 |
|---|---|
| `conv install <目标>` | 安装规则到 `conv/rules/`，默认装 `rules` 版 |
| `conv install all` | 安装全部 4 类语言 |
| `conv install frontend` | 安装前端两个子分类（生成两个独立文件） |
| `conv install python --full` | 装完整版；`--brief` 装精简版 |
| `conv update [语言]` | 用内置最新版覆盖 `conv/rules/`，不动 `conv/project/` |
| `conv list` | 列出可安装语言 + 当前项目已装规则 |
| `conv info` | 显示安装路径、内置文档清单、项目已装情况 |
| `conv show <目标>` | 在终端打印内置文档（预览，不写文件） |
| `conv --version` | 查看版本 |
| `conv --help` | 查看帮助 |

`<目标>` 取值：`python` / `sql` / `frontend-structure` / `frontend-style`，或别名 `all` / `frontend`。

## 行为约定

- **重复执行覆盖**：`install` 直接覆盖已存在的 `conv/rules/*.md`。
- **首次安装建模板**：`conv/project/*.md` 不存在时自动创建引导模板，已存在则不动。
- **`update` 不碰 `conv/project/`**：只更新 `conv/rules/`，保护用户写的项目规则。
- **系统目录拒绝运行**：在 `C:\Windows`、`Program Files` 等系统目录执行会报错退出。
- **版本头**：`conv/rules/*.md` 首行标注 `conv` 版本、安装日期、来源文档，方便溯源。
- **剔除引用行**：写入 `conv/rules/` 时自动删除指向 brief/full/project 等文件的交叉引用句，避免安装后死链（详见"安装"一节）。
- **不进 git**：安装时自动把 `conv/` 加入项目 `.gitignore`。
- **`--dry-run`**：`install` / `update` 加此参数只打印将要写入的文件，不落盘。

## 示例

```bash
cd my-project
conv install python            # 装 Python 最简规则
conv install frontend          # 装前端两个子分类
conv install sql --full        # 装 SQL 完整版
conv info                      # 看安装在哪、装了哪些
conv update                    # 全部更新到内置最新版
```
