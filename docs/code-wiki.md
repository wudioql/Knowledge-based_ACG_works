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
        │   BaseLayout · DocLayout                   │
        │   TimelineLayout · GalleryLayout            │
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
        │   utils/works.ts · utils/toc.ts             │
        └────────────────────────────────────────────┘
```

### 设计思想

1. **数据流单向**：`内容（MDX）` → `数据层（Zod）` → `组件` → `布局` → `页面` → `静态 HTML`
2. **内容创作者与开发者解耦**：新增作品只需在 `content/` 中添加 MDX 文件，不碰任何代码
3. **Fail-fast**：任何不符合 Schema 的 frontmatter 都会让构建立即失败，防止坏数据上线
4. **主题可插拔**：通过在 `<body>` 上添加 `.theme-ocean / .theme-crimson / .theme-amber` 实现
5. **零 JS by default**：Astro 默认不打包运行时 JS；搜索、ScrollSpy 通过小脚本按需注入

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
    defaultThemePalette: z.enum(['ocean', 'crimson', 'amber']).default('ocean'),
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
    themePalette: z.enum(['ocean', 'crimson', 'amber']).optional(),
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

## 3. 数据读取工具（`src/utils/works.ts`）

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

### 设计要点

- 使用 `id.startsWith(workSlug + '/')` 作为过滤约定 — 这依赖 Astro Content Collections 的默认 ID 策略（`目录/文件名`）
- `extractChapterSlug` 会剥离 `.mdx / .md` 扩展名，以确保 `/works/dr-stone/chapter-01/` 而不是 `/works/dr-stone/chapter-01.mdx/`
- 所有排序都在 `getChapters / getWorks` 内完成，页面层直接取用即可

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

随后根据 `layoutType` 选择不同的布局组件 (`DocLayout / TimelineLayout / GalleryLayout`)。

---

## 5. 布局模板（`src/layouts/`）

### BaseLayout

所有页面的外壳。职责：
- 注入全局 CSS（`theme.css`）
- 注入 `<ViewTransitions />` 以启用页面动画
- 设置 `<body>` 的主题类（`theme-ocean / theme-crimson / theme-amber`）
- 渲染站点 header（含搜索按钮）与 footer

```tsx
<BaseLayout title="作品名" theme="crimson">
  <!-- 页面主体 -->
</BaseLayout>
```

### DocLayout — 三栏文档

最适合长篇剧情与设定类章节：

```
┌──────────┬──────────────┬────────┐
│ 章节目录  │   正文内容    │ 动态TOC │
│ (side-nav)│  (article)   │  (toc) │
└──────────┴──────────────┴────────┘
```

- 左栏：作品内章节目录（由上层页面传 `sideNavHtml` 字符串渲染）
- 中栏：Markdown/MDX 渲染的正文
- 右栏：TableOfContents，解析 `h2/h3/h4` 生成，配合 ScrollSpy 高亮

### TimelineLayout — 编年史

```
· 2000 — 第二次冲击
   │
   ├── 南极出现光之巨人
   └── 全球海平面上升
   │
· 2015 — 使徒来袭
```

配合 MDX 组件 `<TimelineNode>` 编写内容：

```mdx
<TimelineNode year="2015" title="使徒来袭">
  第三使徒出现在第三新东京市。
</TimelineNode>
```

### GalleryLayout — 网格图鉴

响应式 CSS Grid，适合角色图鉴、设定图集。配合 `<ImageGallery>` 与 `<Card>` 使用。

---

## 6. 主题系统（`src/styles/theme.css`）

基于 CSS 变量的主题实现，核心思想：

```css
:root {
  --bg-color: #0f172a;
  --text-main: #e2e8f0;
  --accent-primary: #38bdf8;
}

body.theme-ocean   { --accent-primary: #38bdf8; ... }
body.theme-crimson { --accent-primary: #f43f5e; ... }
body.theme-amber   { --accent-primary: #f59e0b; ... }
```

### 为什么不用 class-in-js

- **零运行时代价**：纯 CSS，客户端无需 JS 来切换主题
- **易于扩展**：想添加 `theme-neon`？新增一个选择器即可，不碰代码
- **构建时注入**：主题类由 Astro 静态输出，被 Pagefind 索引时也能正确分类

---

## 7. 动态目录（TOC）+ ScrollSpy

### 数据生成：`src/utils/toc.ts`

- 从 Markdown 的 `headings`（`{ depth, text, slug }`）筛选 `h2/h3/h4`
- 页面层通过 `render()` 方法获取头信息：

```ts
const { Content, headings } = await chapter.render();
const toc = buildToc(headings);  // 之后交给 TableOfContents 组件
```

### ScrollSpy：DOM Script（`src/layouts/DocLayout.astro` 中的内联 script）

```js
const links = document.querySelectorAll('.toc-link');
const headings = document.querySelectorAll('h2, h3, h4');

// IntersectionObserver
const observer = new IntersectionObserver((entries) => {
  const visible = entries.filter((e) => e.isIntersecting)
                         .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
  if (visible.length > 0) {
    const id = visible[0].target.id;
    links.forEach((l) => l.classList.remove('toc-link-active'));
    const match = document.querySelector(`.toc-link[data-target="#${id}"]`);
    if (match) match.classList.add('toc-link-active');
  }
}, { rootMargin: '-120px 0px -70% 0px', threshold: [0, 1] });
```

### 生命周期

| 时机 | 行为 | 说明 |
| --- | --- | --- |
| `DOMContentLoaded` | 初始化 observer + 绑定链接点击 | 首次进入页面 |
| View Transition 完成（`astro:page-load`） | **重建** observer | Astro 的 VT 替换了 DOM 节点，旧 observer 已失效 |
| 页面隐藏 (`visibilitychange`) | **断开** observer | 节省资源 |

**内存泄漏防护要点**：
- 每次导航后不清除旧 observer 会导致内存泄漏 → 通过 `astro:page-load` 重建并在销毁前 `observer.disconnect()`
- 避免对同一元素重复 observe → 在新观察前先 disconnect

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
- **`<script>` 标签中的脚本**在每次导航后都会重新执行（这是 ScrollSpy 得以重建的关键）

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
| `title` | string | 目录标题，默认 "目录" |

**运行时脚本**：由 DocLayout 中的 `<script is:inline>` 负责 ScrollSpy 高亮与平滑滚动

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

## 12. 部署排错指南

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

**已处理**：脚本监听 `astro:page-load` 事件，每次导航后重建 observer。如果仍有问题，请：
- 检查控制台是否有 JS 错误
- 检查 `headings` 数组是否包含有效的 slug

---

## 13. 开发规范

| 事项 | 规范 |
| --- | --- |
| 文件名 | 英文小写，短横线分隔（`my-chapter.mdx`） |
| Frontmatter 字段顺序 | `title` → `order` → `layoutType` → `themePalette` → `tags` → `summary` → `isDraft` |
| 章节 `order` | 用递增整数（1, 2, 3...），便于人工维护 |
| 图像资源 | 统一放 `src/assets/images/`，通过 `<Image>` 或 `<MdxImage>` 引用 |
| 提交前 | 执行 `npm run build`，确保零错误 |

---

## 14. 后续可选扩展

- [ ] 添加 RSS 订阅（`@astrojs/rss`）
- [ ] 引入 Sitemap（`@astrojs/sitemap`）
- [ ] 添加 OG Image / 社交卡片
- [ ] 作品级封面图（`cover` 字段 + 图片组件）
- [ ] Light/Dark 主题切换（目前都是深色基调；可通过 prefers-color-scheme 扩展）
- [ ] 章节评论（Giscus / utterances，纯前端）
