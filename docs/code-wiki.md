# ACG Knowledge Wiki · Code Wiki

本文档面向需要二次开发的贡献者。如果你只需要**新增作品**，请查看 [README.md](../README.md) 中的「5 分钟：新增一个作品」。

---

## 1. 架构分层

```
        ┌────────────────────────────────────────────┐
        │              路由层 (pages/)               │
        │   index.astro · [work]/index.astro         │
        │   [work]/[...slug].astro · 404.astro       │
        └────────────────────┬───────────────────────┘
                             │ 渲染时调用
        ┌────────────────────▼───────────────────────┐
        │             布局层 (layouts/)              │
        │   BaseLayout （含所有交互脚本）              │
        │   DocLayout · TimelineLayout · GalleryLayout │
        └────────────────────┬───────────────────────┘
                             │ 组合
        ┌────────────────────▼───────────────────────┐
        │            组件层 (components/)             │
        │   TableOfContents · WorkNavigator          │
        │   Pagination · SearchBox · MdxImage         │
        │   mdx/Callout · mdx/TimelineNode …          │
        └────────────────────┬───────────────────────┘
                             │ 读取
        ┌────────────────────▼───────────────────────┐
        │          数据层 (content/, utils/)         │
        │   config.ts （Zod Schema）                  │
        │   works/ · chapters/ （MDX 源）              │
        │   utils/works.ts · utils/toc.ts （树形 TOC） │
        └────────────────────────────────────────────┘
```

### 设计思想

1. **数据流单向**：`内容（MDX）` → `数据层（Zod）` → `组件` → `布局` → `页面` → `静态 HTML`
2. **内容创作者与开发者解耦**：新增作品只需在 `content/` 中添加 MDX 文件，不碰任何代码
3. **Fail-fast**：任何不符合 Schema 的 frontmatter 都会让构建立即失败，防止坏数据上线
4. **主题可插拔**：通过在 `<body>` 上添加 `.theme-ocean / .theme-crimson / .theme-amber / .theme-parchment` 实现
5. **零 JS by default**：Astro 默认不打包运行时 JS；搜索、ScrollSpy、侧栏开关通过 BaseLayout 中的 `<script is:inline>` 按需注入（全页面共享，避免重复）

---

## 2. Zod Schema

定义在 `src/content/config.ts`：

```ts
import { defineCollection, z } from 'astro:content';

// 作品级元数据
const works = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    order: z.number().default(0),
    summary: z.string().optional(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    defaultThemePalette: z.enum(['ocean', 'crimson', 'amber', 'parchment']).default('ocean'),
    defaultLayoutType: z.enum(['document', 'gallery', 'timeline']).default('document'),
    isDraft: z.boolean().default(false),
  }),
});

// 章节级元数据
const chapters = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    order: z.number(),
    layoutType: z.enum(['document', 'gallery', 'timeline']).optional(),
    themePalette: z.enum(['ocean', 'crimson', 'amber', 'parchment']).optional(),
    tags: z.array(z.string()).default([]),
    summary: z.string().optional(),
    cover: z.string().optional(),
    isDraft: z.boolean().default(false),
  }),
});

export const collections = { works, chapters };
```

### 关键要点

- **作品与章节分离**：`works/<slug>.mdx` 是作品索引（含简介、默认主题与布局），`chapters/<work>/<slug>.mdx` 是具体章节内容
- **默认值策略**：章节可省略 `themePalette` / `layoutType`，回退为作品的默认值（由页面在渲染时决定）
- **必填字段**：`title`、`order` 为章节级必填 → 这确保了每一章节都能正确排序和展示
- **草稿标记**：`isDraft: true` 的条目在生产构建中被 `getCollection(..., filter)` 过滤掉

---

## 3. 数据读取工具

### 3.1 `src/utils/works.ts`

```ts
import { getCollection } from 'astro:content';

// 作品
export async function getWorks() {
  const works = await getCollection('works', ({ data }) => !data.isDraft);
  return works.sort((a, b) => (a.data.order ?? 0) - (b.data.order ?? 0));
}

// 某作品的所有章节
export async function getChapters(workSlug: string) {
  const all = await getCollection('chapters', ({ data, id }) => {
    if (data.isDraft) return false;
    return id.startsWith(workSlug + '/');   // id 形如 'dr-stone/chapter-01.mdx'
  });
  return all.sort((a, b) => a.data.order - b.data.order);
}

// 从 id 中提取作品 slug
export function extractWorkSlug(id: string): string {
  const idx = id.indexOf('/');
  return idx === -1 ? id : id.slice(0, idx);
}

// 从 id 中提取章节 slug（剥离扩展名）
export function extractChapterSlug(id: string): string {
  const idx = id.indexOf('/');
  const rest = idx === -1 ? id : id.slice(idx + 1);
  return rest.replace(/\.(mdx|md)$/, '');
}
```

### 3.2 `src/utils/toc.ts`（★ 核心工具，被多个布局调用）

**功能概览**：

| 函数 | 作用 | 被调用方 |
| --- | --- | --- |
| `slugify(text)` | 将中文/英文标题转为 URL 友好 slug（`-` 连接，小写） | buildTocTree / buildToc |
| `ensureUnique(slug, seen)` | 保证 slug 在 `seen` Map 中不重复，冲突则追加 `-2`、`-3` | buildTocTree |
| `buildToc(headings)` | 从 `chapter.render()` 的 headings 数组中筛选 h2/h3/h4 | DocLayout（简化版目录） |
| `buildTocTree(headings)` | ★ 生成树结构 `{ depth, text, slug, children: [] }[]`，支持任意层级嵌套 | TableOfContents / [...slug].astro |
| `renderChaptersNav(...)` | 生成章节目录 HTML 字符串（含"全部展开/收起"按钮、逐章折叠） | [...slug].astro 的 `buildChapterNavHtml` |
| `renderTocForRail(...)` | 生成 TOC rail HTML（带 `toc-toggle` 按钮，支持层级展开） | TableOfContents 可选替代 |

**核心数据结构**：

```ts
export interface TocNode {
  depth: number;        // 原始 h2=2, h3=3, h4=4
  text: string;         // 标题文本
  slug?: string;        // URL 锚点
  children: TocNode[];  // 子节点（对于 h2，children 是其下属 h3/h4）
}
```

**`buildTocTree` 算法思想**：

```
输入: [ { depth:2, text:"A" }, { depth:3, text:"B" }, { depth:2, text:"C" } ]

1. 初始化 root = []，stack = []
2. 遍历每个 heading：
   - pop 出所有 stack.depth >= 当前 heading.depth 的节点
   - 如果 stack 为空 → push 到 root
   - 否则 → push 到 stack.top().children
   - 当前节点 push 到 stack
3. 输出 root 作为树根
4. slug 通过 slugify 生成，用 ensureUnique 处理同名标题（罕见但需稳健）
```

### 设计要点

- 使用 `id.startsWith(workSlug + '/')` 作为过滤约定 — 这依赖 Astro Content Collections 的默认 ID 策略（`目录/文件名`）
- `extractChapterSlug` 会剥离 `.mdx / .md` 扩展名，以确保 `/works/dr-stone/chapter-01/` 而不是 `/works/dr-stone/chapter-01.mdx/`
- 所有排序都在 `getChapters / getWorks` 内完成，页面层直接取用即可
- `buildTocTree` 与 `renderChaptersNav` 分离：一个负责数据结构，一个负责 HTML 字符串渲染（便于在 Astro 的 `set:html` 中使用）

---

## 4. 路由层（`src/pages/works/`）

### 动态路由结构

```
src/pages/works/
├── index.astro                  → 作品列表   /<base>/works/
├── [work]/index.astro           → 作品首页   /<base>/works/<work-slug>/
└── [work]/[...slug].astro       → 章节详情   /<base>/works/<work-slug>/<chapter-slug>/
```

### `getStaticPaths` 如何工作

章节详情页通过这段代码枚举所有作品与章节：

```ts
const works = await getWorks();
const paths = [];
for (const w of works) {
  const chapters = await getChapters(w.slug);
  for (const c of chapters) {
    paths.push({
      params: { work: w.slug, slug: extractChapterSlug(c.id) },
      props: { work: w, chapter: c },
    });
  }
}
return paths;
```

这是 Astro SSG 的核心机制：**所有可能的路由都在构建时枚举完成**，没有运行时路由计算。

### 主题 + 布局的选择

```ts
const theme = chapter.data.themePalette ?? work.data.defaultThemePalette;
const layoutType = chapter.data.layoutType ?? work.data.defaultLayoutType;
```

随后根据 `layoutType` 选择不同的布局组件（`DocLayout / TimelineLayout / GalleryLayout`）。

### `buildChapterNavHtml`（在 `[...slug].astro` 中）

这是章节目录 HTML 的生成器。关键点：

1. 为当前章节注入子目录（h2 列表），其他章节不显示子目录（减少页面噪音）
2. 注入"全部展开 / 全部收起"两个按钮，分别控制所有 `.chap-toggle`
3. 序号用两位数 pad（`01`），与作品内排序一致
4. 字符串逃逸用 `escapeHtml`（避免章节标题含 `<` / `>` 导致 XSS）

```
┌──────────────────────────────────────┐
│  《作品名》章节   全部展开  全部收起  │ ← .chap-nav-header
├──────────────────────────────────────┤
│  ▸ 01 第一章 · 使徒来袭 ← .chap-item │
│  ▸ 02 第二章 · 人类补完计划          │ ← 有子目录时显示 toggle icon
│    └─ 关键事件                       │ ← .chap-sub-item 展开后可见
│       └─ 登场角色                    │
└──────────────────────────────────────┘
```

---

## 5. 布局模板（`src/layouts/`）

### 5.1 BaseLayout（★ 所有页面的外壳）

**职责**：
- 注入全局 CSS（`theme.css`）
- 注入 `<ViewTransitions />` 以启用页面动画
- 设置 `<body>` 的主题类（`theme-ocean / theme-crimson / theme-amber / theme-parchment`）
- 渲染站点 header（含搜索按钮）与 footer
- **注入全站交互脚本**（`<script is:inline>`）：
  - 侧栏（章节目录）开关
  - 章节目录的"全部展开/收起"与逐章切换
  - TOC rail 的层级展开、平滑滚动与 ScrollSpy 高亮
  - TOC popover（窄屏）开关
  - Esc 键关闭抽屉

**脚本监听的生命周期**：
- `DOMContentLoaded` → 初始化
- `astro:page-load` → VT 切换后重新初始化（重建 observer、重新绑定事件）
- `astro:after-swap` → 同上（双保险，确保新 DOM 被扫描到）

**内存管理**：
- IntersectionObserver 在每次重建时 disconnect 旧实例
- 通过 `querySelectorAll` 选择时只查询当前文档中的元素
- 事件委托（`.chap-nav` 的 click 事件）避免对每个 toggle 单独 addEventListener

### 5.2 DocLayout — 三栏文档

最适合长篇剧情与设定类章节：

```
┌────────────┬─────────────────────────┬─────────────┐
│ 章节目录    │   正文内容               │ 动态 TOC    │
│ (side-nav)  │  (article, <Content/>)   │ (toc-rail)  │
│ sticky      │  120ch max-width          │ sticky      │
└────────────┴─────────────────────────┴─────────────┘
```

- **左栏**：`chaptersNavHtml` 字符串渲染（由 `[...slug].astro` 构建）
- **中栏**：`chapter.render()` 的 `<Content />`，支持 MDX 组件
- **右栏**：`TableOfContents` 组件，mode="rail"，配合 ScrollSpy 高亮
- **窄屏**：左栏变为抽屉（side-nav-open 类 + CSS transform），右栏变为 action bar 中的 "📑 目录" 弹出层

### 5.3 TimelineLayout — 编年史

```
┌────────────┬─────────────────────────┐
│ 章节目录    │   时间线内容             │
│ (side-nav)  │ (TimelineNode 垂直排列) │
└────────────┴─────────────────────────┘
```

配合 MDX 组件 `<TimelineNode>` 编写内容。与 DocLayout 共享左侧章节目录，但不使用右侧 TOC rail。

### 5.4 GalleryLayout — 网格图鉴

```
┌────────────┬─────────────────────────┐
│ 章节目录    │   图鉴卡片网格           │
│ (side-nav)  │ (CSS Grid auto-fill)    │
└────────────┴─────────────────────────┘
```

响应式 CSS Grid（`repeat(auto-fill, minmax(220px, 1fr))`），适合角色图鉴、设定图集。配合 `<ImageGallery>` 与 `<Card>` 使用。

### 三布局对比

| 特性 | DocLayout | TimelineLayout | GalleryLayout |
| --- | --- | --- | --- |
| 左章节目录 | ✅ | ✅ | ✅ |
| 右 TOC rail | ✅ | ❌ | ❌ |
| 窄屏 TOC 弹出层 | ✅ | ❌ | ❌ |
| reader-action-bar（返回+章节） | ✅ | ✅ | ✅ |
| 主题变量继承 | ✅ | ✅ | ✅ |

---

## 6. 主题系统（`src/styles/theme.css`）

### 6.1 统一的 CSS 变量（★ 核心原则：所有视觉样式都走变量）

```css
:root {
  /* 排版 */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Consolas", "Liberation Mono", monospace;
  --radius: 10px;
  --radius-sm: 6px;
  --radius-lg: 16px;

  /* 阴影 */
  --shadow-sm: 0 1px 4px rgba(0, 0, 0, 0.08);
  --shadow: 0 2px 16px rgba(0, 0, 0, 0.10);
  --shadow-hover: 0 8px 32px rgba(0, 0, 0, 0.18);

  /* 颜色（ocean 默认：墨蓝青） */
  --bg-color: #0e1a1f;
  --bg-elevated: #1a2b36;
  --text-main: #e0f2fe;
  --text-muted: #7a94a3;
  --accent-primary: #22d3ee;    /* 青色海面反光 */
  --accent-secondary: #67e8f9;  /* 亮青 */
  --accent-tertiary: #a78bfa;   /* 紫 */
  --border-color: #243c4d;
  --code-bg: #1a2b36;

  /* 滚动条 */
  --scrollbar-track: transparent;
  --scrollbar-thumb: rgba(103, 232, 249, 0.28);
  --scrollbar-thumb-hover: var(--accent-primary);

  /* 文本选中 */
  --selection-bg: color-mix(in srgb, var(--accent-primary) 30%, transparent);

  /* 分隔线 */
  --hr-color: color-mix(in srgb, var(--border-color) 65%, transparent);

  /* kbd 键盘提示 */
  --kbd-bg: var(--bg-elevated);
  --kbd-border: var(--border-color);

  /* Callout 语义色（info/warning/success/note） */
  --callout-info: #22d3ee;
  --callout-warning: #f59e0b;
  --callout-success: #10b981;
  --callout-note: #a78bfa;

  /* Aside 边注色 */
  --aside-accent: #818cf8;

  /* dialog / popover 遮罩 */
  --dialog-backdrop: rgba(14, 26, 31, 0.68);

  /* focus ring（可访问性） */
  --focus-ring: 0 0 0 2px var(--bg-color), 0 0 0 4px var(--accent-primary);
}
```

### 6.2 四套主题重写（通过选择器覆盖）

```css
body.theme-ocean {
  /* 墨蓝青：冷色科幻 / 海洋主题 —— 继承 :root 默认值 */
  --callout-info: #22d3ee;
  --callout-note: #a78bfa;
}

body.theme-crimson {
  /* 玫瑰胭脂：暖色，情感 / 战斗向作品 */
  --bg-color: #1f0d0d;
  --bg-elevated: #2d1414;
  --text-main: #fde2e2;
  --text-muted: #a57373;
  --accent-primary: #fb7185;    /* 玫瑰粉 */
  --accent-secondary: #f472b6;
  --accent-tertiary: #fcd34d;   /* 暖金，作为对比点缀 */
  --border-color: #4c1d24;
  --code-bg: #2d1414;
  --scrollbar-thumb: rgba(251, 113, 133, 0.28);
  --selection-bg: color-mix(in srgb, var(--accent-primary) 28%, transparent);
  --callout-info: #60a5fa;
  --callout-success: #34d399;
  --callout-note: #f472b6;
  --aside-accent: #f472b6;
  --dialog-backdrop: rgba(31, 13, 13, 0.72);
}

body.theme-amber {
  /* 青铜金：沉郁的古代/沙漠/蒸汽朋克 */
  --bg-color: #1a1410;
  --bg-elevated: #2b2218;
  --text-main: #fef3c7;
  --text-muted: #a89678;
  --accent-primary: #d97706;    /* 琥珀橙 */
  --accent-secondary: #fbbf24;
  --accent-tertiary: #fb923c;
  --border-color: #4a3322;
  --code-bg: #2b2218;
  --scrollbar-thumb: rgba(251, 191, 36, 0.28);
  --selection-bg: color-mix(in srgb, var(--accent-primary) 28%, transparent);
  --callout-info: #60a5fa;
  --callout-note: #fbbf24;
  --aside-accent: #fbbf24;
  --dialog-backdrop: rgba(26, 20, 16, 0.72);
}

body.theme-parchment {
  /* 羊皮卷：浅色主题，古典文学/编年史/魔法书 —— 注意这是唯一的浅色主题 */
  --bg-color: #f5f1e6;
  --bg-elevated: #ebe4d2;
  --text-main: #1c1917;
  --text-muted: #57534e;
  --accent-primary: #7c2d12;    /* 深红棕（古典标题色） */
  --accent-secondary: #92400e;  /* 金棕 */
  --accent-tertiary: #a2641c;   /* 琥珀 */
  --border-color: #c9b88a;
  --code-bg: #e8dfc8;
  --scrollbar-thumb: rgba(124, 45, 18, 0.28);
  --scrollbar-thumb-hover: rgba(124, 45, 18, 0.55);
  --selection-bg: color-mix(in srgb, var(--accent-primary) 25%, transparent);
  --hr-color: color-mix(in srgb, var(--border-color) 80%, transparent);
  --callout-info: #0891b2;
  --callout-warning: #d97706;
  --callout-success: #059669;
  --callout-note: #7c3aed;
  --aside-accent: #7c3aed;
  --kbd-bg: #ebe4d2;
  --kbd-border: #c9b88a;
  --dialog-backdrop: rgba(28, 25, 23, 0.45);
  --shadow-sm: 0 1px 3px rgba(92, 51, 23, 0.08);
  --shadow: 0 2px 12px rgba(92, 51, 23, 0.10);
  --shadow-hover: 0 8px 28px rgba(92, 51, 23, 0.16);
  --focus-ring: 0 0 0 2px var(--bg-color), 0 0 0 4px var(--accent-primary);
}
```

> **设计原则**：三深一浅。三套深色主题共享底色与滚动条基础风格，通过 `accent-primary` 决定情感基调；`parchment` 作为唯一的浅色主题，所有变量必须单独定义。

### 6.3 滚动条统一（跨浏览器）

```css
/* Firefox */
* { scrollbar-width: thin; scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track); }
/* WebKit */
*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-track { background: var(--scrollbar-track); }
*::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: 999px;
  transition: background-color 0.2s ease;
}
*::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-thumb-hover); }
```

**窄屏降级**：≤720px 时 `::-webkit-scrollbar { display: none }`，避免触控设备上视觉噪音。

### 6.4 响应式断点与 z-index 栈

```css
/* 断点（三个布局共享同一套断点） */
/* ≤720px  → 窄屏，单栏，抽屉式 side-nav，固定 action-bar */
/* 720–1100px → 平板，三栏但宽度缩减 */
/* >1100px  → 宽屏，完整三栏 */

/* z-index 栈（约定值，全项目统一，避免互相覆盖） */
/* 98  →  .nav-overlay（章节目录的遮罩） */
/* 99  →  .side-nav（章节目录抽屉） */
/* 100 →  .reader-action-bar（顶部固定操作栏） */
/* 101 →  .toc-popover（本章目录弹出层） */
/* 200 →  search dialog（搜索框，用 <dialog> 原生 top-layer） */
```

### 为什么不用 class-in-js

- **零运行时代价**：纯 CSS，客户端无需 JS 来切换主题
- **易于扩展**：想添加 `theme-neon` 或 `theme-forest`？新增一个选择器即可，不碰代码；若需语义色或浅色主题，别忘了新增 `--callout-*` 与 `--aside-accent` 等变量
- **构建时注入**：主题类由 Astro 静态输出，被 Pagefind 索引时也能正确分类

---

## 7. 动态目录（TOC）+ ScrollSpy

### 7.1 数据生成：`src/utils/toc.ts` 的 `buildTocTree`

- 从 Markdown 的 `headings`（`{ depth, text, slug }`）筛选 `h2/h3/h4`
- 页面层通过 `chapter.render()` 获取 headings，再传给 `TableOfContents` 组件

### 7.2 组件：`src/components/TableOfContents.astro`

```tsx
<aside class:list={["toc-rail", "toc-rail-mode-" + mode]}>
  <div class="toc-rail-header">{title}</div>
  {root.map((node) => (
    <div class="toc-row">
      {node.children.length > 0 && (
        <button type="button" class="toc-toggle" aria-expanded="false"
                aria-controls={`toc-${node.slug}`} aria-label={`展开 ${node.text}`}>
          <span class="toc-toggle-icon">▸</span>
        </button>
      )}
      <a class="toc-link" href={`#${node.slug}`} data-target={`#${node.slug}`}>{node.text}</a>
    </div>
    {node.children.length > 0 && (
      <div class="toc-children" id={`toc-${node.slug}`} hidden>
        {/* 递归渲染子节点 */}
      </div>
    )}
  ))}
</aside>
```

**两种 mode**：
- `mode="rail"`（宽屏右侧）：sticky 定位，带滚动条美化
- `mode="popover"`（窄屏弹出）：点击 action bar 的 "📑 目录" 打开，浮层式

### 7.3 ScrollSpy：DOM Script（BaseLayout 中）

```js
const links = Array.from(document.querySelectorAll('.toc-link'));
if (links.length === 0) return;

// 收集目标标题
const hEls = [];
for (const link of links) {
  const href = link.getAttribute('data-target') || link.getAttribute('href') || '';
  if (!href.startsWith('#')) continue;
  const id = href.slice(1);
  const h = document.getElementById(id);
  if (h) hEls.push(h);
}

// IntersectionObserver
const obs = new IntersectionObserver((entries) => {
  const visible = entries
    .filter((e) => e.isIntersecting)
    .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
  if (visible.length > 0) {
    const id = visible[0].target.id;
    requestAnimationFrame(() => {
      links.forEach((l) => l.classList.remove('toc-link-active'));
      const match = document.querySelector(`.toc-link[data-target="#${id}"]`);
      if (match) match.classList.add('toc-link-active');
    });
  }
}, { rootMargin: '-120px 0px -70% 0px', threshold: [0, 1] });

hEls.forEach((h) => obs.observe(h));
```

**rootMargin 说明**：`-120px 0px -70% 0px` 表示「标题至少滚到视口上方 120px 以下，且尚未被滚出下方 70% 以外」才算可见。这比默认更贴近阅读视线。

### 7.4 生命周期

| 时机 | 行为 | 说明 |
| --- | --- | --- |
| `DOMContentLoaded` | 初始化 observer + 绑定链接点击 | 首次进入页面 |
| View Transition 完成（`astro:page-load`） | **重建** observer | Astro 的 VT 替换了 DOM 节点，旧 observer 已失效 |
| `astro:after-swap` | 重建（双保险） | 与 page-load 同时触发，确保某些页面先 swap 再 load |

**内存泄漏防护要点**：
- 每次导航后不清除旧 observer 会导致内存泄漏 → 通过 `astro:page-load` 重建前在逻辑上隐式 GC（旧 observer 不再被任何地方引用）
- 避免对同一元素重复 observe → 在新观察前使用 `disconnect()` 清除旧实例
- 使用事件委托在 `.toc-rail` 上监听点击，而不是给每个链接单独加监听

---

## 8. View Transitions 在 Astro 中的使用

### 启用

在 `BaseLayout.astro` 的 `<head>` 中：

```astro
<ViewTransitions />
```

### 行为

- 同域链接点击 → 触发 transition（fade + 轻微位移）
- 旧 DOM 淡出 → 新 DOM 淡入
- `<title>` 自动更新
- **`<script is:inline>` 的脚本**在每次导航后都会重新执行（这是 ScrollSpy 得以重建的关键）

### 动画自定义

在 `theme.css` 中定义：

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.35s;
}
```

### 陷阱

- View Transitions 只在支持的浏览器生效（Chrome 111+、Safari 18+）；不支持时回退为普通导航
- `<script is:inline>` 的脚本在 VT 后也会重新执行，注意副作用的幂等性
- `<base>` 标签配合 Astro 的 `import.meta.env.BASE_URL` 处理路由路径

---

## 9. Pagefind 站内搜索

### 工作流程

```
npm run build
  → Astro 输出静态页面到 dist/
  → postbuild 钩子自动执行: pagefind --site dist
    → 扫描所有 HTML, 中文分词
    → 生成 dist/pagefind/*.pf_* 索引
  → npm run preview （或部署到 GitHub Pages）
    → 浏览器中搜索框加载 /<base>/pagefind/pagefind.js
    → 键入时即时匹配并展示结果
```

### 搜索 UI

`<SearchBox />` 组件包含：
- 顶栏的搜索按钮（点击打开 `<dialog>`）
- 搜索输入框（输入即搜索）
- 通过 `<script is:inline>` 懒加载 `pagefind.js`
- 结果 URL 由 Pagefind 自动生成并带上 base 路径

**快捷键**：Ctrl/⌘ + K 唤起搜索框

### 常见问题

| 症状 | 原因 | 解决 |
| --- | --- | --- |
| 点击搜索按钮后无结果 | `dist/pagefind/` 缺失或 base 路径不对 | 确认 `postbuild` 正常执行；检查浏览器 Network 中 `pagefind.js` 是否 200 |
| 本地 dev 环境搜不到内容 | 只有 build 后才生成索引 | 使用 `npm run build && npm run preview` |
| 中文单字匹配不到 | Pagefind 的中文分词是逐字切分 | 这是已知行为，对长词匹配仍然有效 |

---

## 10. 图像管线（`MdxImage.astro` + `astro:assets`）

```astro
import { Image } from 'astro:assets';

<Image
  src={resolved}
  alt={alt}
  widths={[320, 640, 960, 1280]}
  sizes="(max-width: 640px) 92vw, (max-width: 1100px) 60vw, 720px"
  loading="lazy"
  decoding="async"
  format={['avif', 'webp']}
  quality={82}
/>
```

**作用**：
- 根据访问者的视口尺寸选择合适分辨率
- 自动转 AVIF（浏览器支持时），回退到 WebP / 原始格式
- `width/height` 由 Astro 从源图片读取，避免布局抖动（Cumulative Layout Shift）
- `loading="lazy"` 与 `decoding="async"` 让首屏更快

**使用建议**：
- 图片放到 `src/assets/images/` 下（会被 astro:assets 处理）
- 不直接用 `<img>`；在 MDX 里需要响应式图片时用 `<MdxImage>`

---

## 11. 组件 API 字典

### 11.1 `WorkNavigator`（作品切换）

| Props | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `currentWorkSlug` | string | undefined | 当前选中作品的 slug；不提供则无高亮 |

**渲染结果**：一组 pill 样式的链接（作品 1 / 作品 2 / …）

### 11.2 `Pagination`（章节翻页）

| Props | 类型 | 说明 |
| --- | --- | --- |
| `prevHref` | string | 上一章链接；空串则显示"已是第一章" |
| `prevTitle` | string | 上一章标题 |
| `nextHref` | string | 下一章链接 |
| `nextTitle` | string | 下一章标题 |

### 11.3 `TableOfContents`

| Props | 类型 | 说明 |
| --- | --- | --- |
| `headings` | `{ depth, text, slug? }[]` | 从 `chapter.render()` 获取 |
| `title` | string | 目录标题，默认 "本章目录" |
| `mode` | `"rail" \| "popover"` | rail=宽屏右侧 rail；popover=窄屏浮层 |

**运行时脚本**：由 BaseLayout 中的脚本负责：
- `.toc-toggle` 点击 → 展开/收起子目录
- `.toc-link` 点击 → 平滑滚动到目标 + 更新 `data-target`
- IntersectionObserver → 给当前段落加 `toc-link-active` 类

### 11.4 `SearchBox`

无 Props。通过 `<meta name="base-url">` 读取 base 路径。

### 11.5 MDX 组件集合（`src/components/mdx/*.astro`）

| 组件 | Props | 用途 |
| --- | --- | --- |
| `Callout` | `type: 'info\|warning\|success\|note'`, `title` | 提示块/警告/标注 |
| `HeroCard` | `title`, `icon`, `accent` | 大图标 + 渐变色的强调块 |
| `Card` | `title`, `subtitle` | 普通的内容卡片 |
| `ImageGallery` | `columns`, `gap` | 图片网格容器（内部放 `<img>` 或 `<MdxImage>`） |
| `TimelineNode` | `year`, `date`, `title` | 时间线节点，配合 `TimelineLayout` 使用 |
| `InfoGrid` | `items: [{ label, value }]` | 键值对网格（角色资料等） |
| `Quote` | `cite` | 带署名的引用块 |
| `Divider` | `text` | 分隔线，可带文字 |
| `TagList` | `items: string[]`, `heading` | 标签列表块 |
| `Aside` | `title`, `position: 'left\|right'` | 侧边注（桌面端浮动，移动端堆叠） |

### 11.6 `LazySection`（按需加载）

通过 IntersectionObserver 在滚入视口时添加动画，视觉上是懒浮现效果（**不做代码拆分**，只是动画延迟）。

---

## 12. 响应式设计要点（★ 新增/优化章节）

### 12.1 断点策略

```
≥ 1100px  宽屏 → 三栏完整布局，左栏 sticky，右栏 TOC rail
720–1100px 平板 → 三栏宽度缩减，左栏 min-width 180px，字号略小
≤ 720px  窄屏 → 单栏，左栏变抽屉，action-bar 固定顶部
```

**所有布局（Doc/Timeline/Gallery）共用同一套断点**，这确保用户在不同内容间切换时交互一致性。

### 12.2 窄屏 Action Bar（`.reader-action-bar`）

```
┌──────────────────────────────────────────┐
│ ← 返回《作品名》   ☰ 章节   📑 目录  │
└──────────────────────────────────────────┘
```

- 固定定位：`position: sticky; top: 0; z-index: 100`
- flex 布局：`justify-content: space-between`（左:返回+章节，右:目录）
- 交互按钮统一 `.btn-sm`，内联 icon + 文字

### 12.3 z-index 栈（严格约定）

这是防止控件互相覆盖的核心设计：

| 值 | 元素 | 说明 |
| --- | --- | --- |
| 98 | `.nav-overlay` | 章节目录抽屉的半透明遮罩，点击关闭抽屉 |
| 99 | `.side-nav` | 章节目录抽屉本体（从左侧滑出） |
| 100 | `.reader-action-bar` | 顶部操作栏，始终可见 |
| 101 | `.toc-popover` | 本章目录弹出层（需浮在 action-bar 之上） |
| 200 | `<dialog>` | 搜索对话框（原生 top-layer，z-index 保险） |

**避免在其他组件中添加更高的 z-index**；如果需要新的浮层，先在本表中登记新值。

### 12.4 可访问性（A11y）

- 所有可交互按钮都有 `aria-label`（在窄屏纯图标模式下读屏器仍可用）
- `toc-toggle` / `chap-toggle` 有 `aria-expanded` 指示展开状态，`aria-controls` 指向受控元素的 ID
- 折叠容器有 `hidden` 属性（CSS 不起作用，真正意义上不可被键盘聚焦）
- Esc 键关闭所有浮层（侧栏 + TOC popover）
- `--focus-ring` 为焦点元素提供 2px bg + 4px accent 的双层高亮（在深色主题下对比度足够）
- `<dialog>` 元素为原生语义，自带模态背景和焦点管理

---

## 13. 部署排错指南

### 问题 A：CSS / JS / 图片全部 404（首页是白的）

**最可能原因**：base 路径错误

- Astro 配置中的 `base` 与页面实际部署的路径前缀不一致
- 例如：部署到 `https://user.github.io/my-wiki/`，但 `base` 是 `/Knowledge-based_ACG_Astro_Wiki/`

**诊断**：
```bash
# 查看 astro.config.mjs 中的 base 值
grep -n base astro.config.mjs
# 或通过环境变量覆盖
BASE_PATH=/my-wiki/ npm run build
```

**GitHub Pages CI**：`.github/workflows/deploy.yml` 已经通过 `steps.base` 自动把 base 设置为 `/<repo-name>/`，一般不需要手动改。

### 问题 B：搜索框输入后"无结果"

**诊断**：
- `npm run build` 的输出是否有 `pagefind` 日志？
- `ls dist/pagefind/` 下是否有 `.pf_index` / `.pf_meta` 文件？
- 浏览器 DevTools → Network，是否 `pagefind.js` 返回 404？

**修复**：
- 确保 `package.json` 里有 `"postbuild": "pagefind --site dist"`
- 确保 pagefind 已安装：`npm ls pagefind`（应出现在 devDependencies）

### 问题 C：构建失败 — "Expected number, received string"

**原因**：frontmatter 中 `order` 写成了字符串，Zod 类型校验失败

```mdx
---
title: 第一章
order: "1"   # ❌ 这是字符串
---
```

**修复**：去掉引号 → `order: 1`

### 问题 D：新增的作品在站点上没显示

**排查清单**：

1. ✅ `src/content/works/<slug>.mdx` 是否存在？
2. ✅ 作品文件的 `isDraft` 是 `false` 吗？
3. ✅ `src/content/chapters/<work-slug>/` 目录下至少有 1 个章节吗？
4. ✅ 章节的 `order` 是数字且不重复吗？
5. ✅ 执行了 `npm run build` 且无错误吗？

### 问题 E：View Transitions 切换后 TOC 不高亮

**原因**：IntersectionObserver 是在旧 DOM 的元素上注册的，被 Astro VT 替换后失效。

**已处理**：BaseLayout 脚本监听 `astro:page-load` + `astro:after-swap` 事件，每次导航后重建 observer。如果仍有问题，请：
- 检查控制台是否有 JS 错误
- 检查 `headings` 数组是否包含有效的 slug
- 检查 `h2/h3/h4` 元素是否真的有 `id` 属性（由 Astro 自动生成，但特殊字符可能被转义）

### 问题 F：TOC 弹出层被 action-bar 覆盖

**原因**：z-index 顺序错误

**修复**：确保 `toc-popover` 的 z-index 高于 `reader-action-bar`（约定 101 vs 100）

---

## 14. 开发规范

| 事项 | 规范 |
| --- | --- |
| 文件名 | 英文小写，短横线分隔（`my-chapter.mdx`） |
| Frontmatter 字段顺序 | `title` → `order` → `layoutType` → `themePalette` → `tags` → `summary` → `isDraft` |
| 章节 `order` | 用递增整数（1, 2, 3...），便于人工维护 |
| 图像资源 | 统一放 `src/assets/images/`，通过 `<Image>` 或 `<MdxImage>` 引用 |
| 硬编码颜色 | **禁止**。所有颜色、圆角、阴影、边框都应使用 `theme.css` 中的 CSS 变量 |
| 新增交互脚本 | **放入 BaseLayout.astro 的 `<script is:inline>`**，不要在各个 layout 中重复写 |
| z-index | **禁止随意写大值**。新的浮层必须在"响应式设计要点"章节的 z-index 表中登记 |
| 可访问性 | 新增按钮必须有 `aria-label`；新增折叠控件必须有 `aria-expanded` + `aria-controls` |
| 提交前 | 执行 `npm run build`，确保零错误 |

---

## 15. 后续可选扩展

- [ ] 添加 RSS 订阅（`@astrojs/rss`）
- [ ] 引入 Sitemap（`@astrojs/sitemap`）
- [ ] 添加 OG Image / 社交卡片
- [ ] 作品级封面图（`cover` 字段 + 图片组件）
- [ ] Light/Dark 主题切换（目前都是深色基调；可通过 prefers-color-scheme 扩展）
- [ ] 章节评论（Giscus / utterances，纯前端）
- [ ] 章节内的 h5 支持（目前只到 h4）
