# 前端样式规则清单

只有规则，没有解释和示例。要示例看 [brief.md](brief.md)，要理由看 [full.md](full.md)。

## CSS Module / SCSS 项目

1. 预处理器 less / scss 二选一，同一项目内不混用。
2. 页面组件样式用 CSS Module，文件名与组件同名。
3. Module 内类名用 camelCase。
4. 页面 module 只写布局和页面独有样式，不写公共组件内部样式。
5. 公共组件禁止 CSS Module；内部类名全局，带项目前缀，用 BEM。
6. 外部调整时，在使用方页面的 module 里用 `:global` 穿透。
7. 嵌套不超过 3 层；`!important` 只用于覆盖第三方，且必须注释原因。
8. 状态类名统一用 `is-` 前缀：`is-active` / `is-disabled` / `is-loading` / `is-error`。
9. 单个 module 文件超过 150 行，考虑拆组件, 但应该以组件的功能为主，不能因为module太长而将组件功能拆分。

## Tailwind 项目

1. Tailwind 项目页面用工具类，不写 CSS Module；复杂动画、伪元素用 SCSS。CSS Module / Less / SCSS 项目不引入 Tailwind。
2. 颜色走 `theme.extend.colors`，禁止硬编码 hex；禁止 `bg-[#xxx]` 任意值。
3. 间距用 spacing scale（`p-4`、`gap-3`，1 单位 = 4px）；禁止 `p-[13px]`，非标值扩展 `theme.spacing`。
4. 多个工具类用 `cn`（shadcn-ui 封装：`twMerge` + `clsx`）分组；类太多影响阅读时用 `cn` 拆分。
5. 响应式用断点前缀（`sm:` `md:` `lg:`），移动端优先；断点在 `theme.screens` 定义。
6. 交互状态用前缀（`hover:` `focus:` `active:` `disabled:`），不写伪类 CSS。
7. `@apply` 只用于提取多处复用的工具类组；单处不 `@apply`。
8. 多主题用 `theme` 机制；深色模式也是主题，禁止用 `dark:` 前缀。

## 通用（两者均适用）

1. 有组件库的项目不引入 tailwind。
2. 公共组件根元素必须带组件级类名（如 `xx-save-btn`），作为唯一对外样式入口；有项目前缀则加前缀。
3. 穿透只允许改表现属性（颜色、字号、间距、圆角），不允许改布局结构。
4. 重封装组件库组件时根元素带前缀类名；禁止直接改第三方内部 class。
5. 改样式只允许三种手段，按优先级：theme token → 重封装 → 页面穿透。
6. 全局样式只允许一个文件；组件里禁止 import 全局 css。
7. design token 集中在主题配置里；组件内禁止写死颜色值。
8. 禁止行内 `style`，动态计算值除外。
9. 公共组件文件头必须声明"可覆盖的类名"。
10. 断点集中定义，页面里禁止裸写媒体查询数值。
11. 间距默认取 4 的倍数；无法满足时取偶数；因 1px 边框只能取奇数时，优先改用 flex 居中解决。
12. 样式里不写魔法数字，间距走变量或 4 的倍数。
