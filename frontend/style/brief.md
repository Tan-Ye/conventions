# 前端样式规则 · 精简版

每条规则配一个能直接抄的示例。只有规则看 [rules.md](rules.md)，要理由看 [full.md](full.md)。

## CSS Module / SCSS 项目

| # | 规则 | 示例 |
|---|---|---|
| 1 | 预处理器二选一 | 项目内只用 `scss` |
| 2 | 页面样式用 CSS Module | `OrderEdit.module.scss` |
| 3 | Module 类名 camelCase | `.lineRow` |
| 4 | 页面 module 只写布局 | 不写 `.ant-btn` 覆盖 |
| 5 | 公共组件禁用 Module | `.ui-btn__icon`（全局） |
| 6 | 穿透用 `:global` | `:global(.ui-btn) { ... }` |
| 7 | 嵌套 ≤ 3 层 | `!important` 必须注释 |
| 8 | 状态类名 `is-` 前缀 | `is-loading` |
| 9 | module 超 150 行拆组件 | — |

## Tailwind 项目

| # | 规则 | 示例 |
|---|---|---|
| 1 | Tailwind 项目不用 CSS Module | 复杂动画/伪元素用 SCSS |
| 2 | 颜色走 theme | `bg-primary`，不写 `bg-[#1677ff]` |
| 3 | 间距用 spacing scale | `p-4`、`gap-3` |
| 4 | 多类用 cn 分组 | `cn('flex gap-2', isOpen && 'block')` |
| 5 | 响应式前缀，移动端优先 | `sm:` `md:` `lg:` |
| 6 | 状态用前缀 | `hover:bg-primary` `disabled:opacity-50` |
| 7 | @apply 只提取复用组 | 多处重复才用 |
| 8 | 多主题用 theme，禁 dark: | 深色也是主题 |

## 通用（两者均适用）

| # | 规则 | 示例 |
|---|---|---|
| 1 | 有组件库不引 tailwind | AntD 项目不装 tailwind |
| 2 | 根元素带组件类名 | `<Button className="xx-save-btn">` |
| 3 | 穿透只改表现 | 颜色/字号/间距，不改 `display` |
| 4 | 重封装不改内部 class | 包一层，不写 `.ant-btn-primary` |
| 5 | 三种手段按优先级 | theme → 重封装 → 穿透 |
| 6 | 全局样式只有一个文件 | `src/styles/global.scss` |
| 7 | 颜色走 token | `var(--ui-primary)` |
| 8 | 禁止行内 style | 动态值除外 |
| 9 | 组件头声明可覆盖类名 | JSDoc 列出 `ui-btn__*` |
| 10 | 断点集中定义 | `@include lg { }` |
| 11 | 间距 4 的倍数 | `8 / 12 / 16`，1px 边框优先 flex 居中 |
| 12 | 不写魔法数字 | 间距走变量 |

## 完整示例

```scss
// components/FinButton/index.scss —— 公共组件，全局类名
.ui-btn {
  padding: 0 16px;          // 4 的倍数
  border-radius: var(--ui-radius);   // token，不写死 4px

  &__icon { margin-right: 8px; }
  &.is-loading { opacity: 0.6; }
}
```

```scss
// pages/OrderEdit.module.scss —— 页面，CSS Module
.toolbar {
  display: flex;
  gap: 8px;
}

:global(.ui-btn) {
  :global(.ui-btn__icon) { color: #fff; }   // 只改表现
}
```

```tsx
// Tailwind 项目页面
<div className="flex items-center gap-2 p-4">
  <button className="bg-primary text-white hover:bg-primary-hover">保存</button>
</div>
```
