# 前端样式规范 · 完整版

**适用范围**：所有前端样式代码。项目特有的约定见 [project/frontend-style.md](../../project/frontend-style.md)。
只有规则看 [rules.md](rules.md)，规则加示例看 [brief.md](brief.md)。组件与目录规则见 [../structure/full.md](../structure/full.md)。

**目标**：公共组件的类名和页面的类名互不影响——改一个页面不会波及其他页面，公共组件有一个稳定、可查的样式入口。

本规范分三部分：**CSS Module / SCSS 项目**、**Tailwind 项目**、**通用规则**。前两部分按技术栈选读，通用规则两者都要遵守。

---

# 一、CSS Module / SCSS 项目

## 1. 预处理器

less / scss 二选一，同一项目内不混用。两者能力接近，混用只会让构建多一条链路。

## 2. 页面组件：CSS Module

```scss
// pages/OrderEdit.module.scss
.toolbar { display: flex; gap: 8px; }
.lineRow { padding: 8px 0; }
```

- 文件名与组件同名：`OrderEdit.tsx` ↔ `OrderEdit.module.scss`
- 类名 camelCase：`.lineRow`，不写 `.line-row`——JS 里 `styles.lineRow` 才对得上
- 只写布局和页面独有的表现，不写公共组件的内部样式

CSS Module 的作用是**隔离**：这个页面里的 `.toolbar` 和别的页面的 `.toolbar` 互不影响。

## 3. 公共组件：全局类名 + 前缀 + BEM

公共组件**禁止使用 CSS Module**。理由很直接：Module 会把类名哈希成 `_btn_x7f2a`，外部无法稳定命中，穿透就不成立了。

```scss
// components/UiButton/index.scss
.ui-btn { padding: 0 16px; }
.ui-btn__icon { margin-right: 8px; }
.ui-btn--loading { opacity: 0.6; }
```

```tsx
// components/UiButton/index.tsx
/**
 * 财务项目通用按钮。
 *
 * 可覆盖的类名：
 *   ui-btn           根
 *   ui-btn__icon     图标
 *   ui-btn--loading  加载态
 */
export function UiButton(props: ButtonProps) {
  return <Button className="ui-btn" {...props} />
}
```

公共组件：`前缀-组件` + `__元素` + `--修饰符`。

## 4. 外部怎么改公共组件的样式

在使用方页面的 module 里用 `:global` 穿透：

```scss
// pages/OrderEdit.module.scss
:global(.ui-btn) {
  :global(.ui-btn__icon) { color: #fff; }
}
```

两处都要 `:global`：外层不加，`.ui-btn` 会被哈希；内层不加，`.ui-btn__icon` 也会被哈希。

## 5. 嵌套与优先级

- **嵌套不超过 3 层**，再深就说明结构该拆了
- **`!important` 只用于覆盖第三方库**，且必须写注释说明为什么非它不可

```scss
// 覆盖 AntD 的 message 层级，它的样式优先级比页面高，只能强制
:global(.ant-message) { z-index: 2000 !important; }
```

## 6. 命名

- 状态类统一 `is-` 前缀：`is-active` / `is-disabled` / `is-loading` / `is-error`
- 不用 `.active` / `.on` / `.cur` 这类各写各的

## 7. 可维护性

- 单个 module 文件超过 150 行，说明这个页面该拆组件了

---

# 二、Tailwind 项目

> 本节规则仅适用于**使用 Tailwind 的项目**。CSS Module / Less / SCSS 项目不引入 Tailwind。

## 8. 工具类与 CSS Module 的取舍

Tailwind 项目中，**页面级样式直接写工具类**，不建 `*.module.css`：

```tsx
// ✅ 工具类直接写 JSX
<div className="flex items-center gap-2 p-4">
  <span className="text-primary">标题</span>
</div>
```

只有**复杂动画、伪元素（`::before` / `::after`）、超出工具类表达能力的样式**才用 SCSS 文件，且 SCSS 里仍可通过 `@apply` 引用工具类。

## 9. 颜色走 theme，禁硬编码

颜色统一在 `tailwind.config.js` 的 `theme.extend.colors` 定义，组件内只用语义类名：

```tsx
// ✅ 语义类
<button className="bg-primary text-white">保存</button>

// ✗ 硬编码 / 任意值
<button className="bg-[#1677ff] text-[#fff]">保存</button>
```

## 10. 间距用 spacing scale

Tailwind 默认 1 单位 = 4px，`p-4` = 16px，`gap-3` = 12px，天然符合"间距取 4 的倍数"。禁止写非标任意值：

```tsx
// ✅
<div className="p-4 gap-3" />

// ✗ 非标值，应扩展 theme.spacing
<div className="p-[13px] gap-[6px]" />
```

## 11. 多类用 cn 分组

类名较多或有条件时，用 `cn` 分组，避免一长串字符串影响阅读。`cn` 是 shadcn-ui 的封装（`twMerge` + `clsx`），除了条件拼接，还能自动解决 Tailwind 类冲突（如 `'p-2 p-4'` 只保留 `p-4`）：

```tsx
import { cn } from '@/lib/utils'

// ✅ 分组清晰
<div className={cn(
  'flex items-center gap-2',
  isOpen && 'bg-white shadow',
  disabled ? 'opacity-50' : 'hover:bg-primary'
)} />

// ✅ cn 自动去重冲突类（clsx 做不到，会输出 'p-2 p-4' 靠顺序碰运气）
<Button className="p-4" />  // 内部 'p-2' 与传入 'p-4' 冲突时保留 p-4

// ✗ 一长串难读
<div className={`flex items-center gap-2 ${isOpen ? 'bg-white shadow' : ''} ${disabled ? 'opacity-50' : 'hover:bg-primary'}`} />
```

## 12. 响应式与状态

- 响应式用断点前缀，**移动端优先**：默认样式写移动端，`sm:` `md:` `lg:` 覆盖大屏；断点在 `theme.screens` 统一定义。
- 交互状态用前缀，不写伪类 CSS：

```tsx
// ✅
<button className="hover:bg-primary focus:outline-none disabled:opacity-50" />

// ✗ 不写 :hover
// .btn:hover { background: ... }
```

## 13. @apply 的边界

`@apply` 只在**多处重复同一组工具类**时提取复用，单处样式不 `@apply`（否则等于把 Tailwind 写成了 CSS，失去优势）：

```scss
// ✅ 多处复用才提取
.btn-primary {
  @apply px-4 py-2 rounded bg-primary text-white;
}

// ✗ 单处也 @apply，没必要
.tmp { @apply flex items-center; }
```

## 14. 多主题与深色模式

多主题统一用 Tailwind 的 `theme` 机制。**深色模式也是一个主题**，通过 `theme.extend.colors` 定义不同主题的变量值，由 JS 切换主题类（如 `html` 上的 `theme-dark`）生效。

**禁止使用 `dark:` 前缀**——它把"深色"特殊化，与多主题体系不兼容，且切换宿主不一致时容易出 bug。

## 15. shadcn-ui：拼成项目级基础组件

shadcn-ui 默认生成的组件（如 `components/ui/button.tsx`）不要直接散用。应在其基础上**拼接出项目级基础组件**——收口项目默认的 variant、size 和公共逻辑——供全局使用，保证风格统一。

如果有**不同用途**（项目级组件覆盖不了的场景），直接使用 `ui/` 文件默认导出的组件进行拼接，而不是往项目级组件里塞特例。

```tsx
// ui/button.tsx —— shadcn 默认生成，保持原样不改动

// ✅ 项目级基础组件：收口默认值，全局统一使用
// components/AppButton.tsx
import { Button, type ButtonProps } from '@/components/ui/button'

export function AppButton({ variant = 'default', size = 'md', ...props }: ButtonProps) {
  return <Button variant={variant} size={size} {...props} />
}

// ✅ 不同用途：直接用默认导出的组件拼接，不扩展 AppButton
import { Dialog, DialogTrigger, DialogContent } from '@/components/ui/dialog'
```

---

# 三、通用规则

以下规则 CSS Module / SCSS 项目和 Tailwind 项目均适用。

## 16. 技术选型

**有组件库的项目不引入 tailwind。** AntD、Element 这类库自带样式体系和主题变量，再叠一层原子类，同一个视觉会有两个来源，改起来先要判断"这条样式是谁生效的"。

没有组件库、纯自绘的项目，tailwind 很划算。

## 17. 公共组件的类名入口

公共组件根元素必须带**组件级类名**（如 `xx-save-btn`），这是唯一的对外样式入口。前缀避免两个组件都叫 `.header` 撞车。

Tailwind 项目中同样适用：不能只有工具类没有语义类名——否则主题切换和外部覆盖都无法精确定位。

## 18. 穿透的边界

穿透（`:global` 或 Tailwind 中对公共组件类名的覆盖）**只允许改表现属性**：颜色、字号、间距、圆角。不允许改布局结构（`display`、`position`、子元素顺序）——结构有意见就改组件本身，否则组件内部永远不能重构。

## 19. 重封装优于直接改第三方

重封装组件库组件时根元素带前缀类名；**禁止直接改第三方内部 class**（如 `.ant-btn-primary`）。

直接写第三方内部 class 的问题：类名是库的私有实现，升级即失效，而且散落在各处无法统计。

## 20. 改样式的优先级

只允许三种手段，按顺序取第一个能满足的：

| 顺序 | 手段 | 场景 |
|---|---|---|
| 1 | 主题配置（`ConfigProvider` 的 `theme.token` / `components`，或 Tailwind 的 `theme`） | 全局视觉统一改 |
| 2 | 重封装组件 + 前缀类名 | 某个组件的标准样式不同 |
| 3 | 页面穿透 | 单页的一次性调整 |
| ✗ | 直接写第三方内部 class | **禁止** |

## 21. 全局样式与 design token

**全局样式只允许一个文件**：`src/styles/global.scss`，只放 reset 和 CSS 变量。组件里禁止 `import` 全局 css——打包顺序不可控，同一个选择器在不同页面可能表现不同。

**design token 集中管理**（CSS 变量或 Tailwind `theme.extend`）：

```scss
:root {
  --ui-primary: #1677ff;
  --ui-radius: 4px;
  --ui-gap: 8px;
}
```

组件内禁止写死 `#1677ff`。颜色改一次要改二十个文件，就是从这里开始的。

## 22. 禁止行内 style

禁止行内 `style`，动态计算值（按数据算的宽度百分比）除外——行内样式优先级最高，会把上面整套优先级打乱。

## 23. 公共组件声明可覆盖类名

公共组件文件头必须声明"可覆盖的类名"——否则外部用的时候只能翻源码猜。

## 24. 断点集中定义

断点集中定义，页面里禁止裸写媒体查询数值：

```scss
// global.scss
@mixin lg { @media (min-width: 1200px) { @content; } }
```

Tailwind 项目在 `theme.screens` 定义。

## 25. 数值

**间距默认取 4 的倍数**：4 / 8 / 12 / 16 / 24 / 32。

无法满足时取偶数。**因为 1px 边框导致只能取奇数时，优先改用 flex 居中来规避**——比如"高度 31px 的按钮"，正确做法是 `height: 32px` + `display: flex; align-items: center`，而不是把 padding 写成 7px 去凑。

样式里不写魔法数字，间距走变量或 4 的倍数。
