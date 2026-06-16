# ACG Knowledge Wiki · Astro 知识库

> 基于 [Astro 5](https://astro.build) + [Pagefind](https://pagefind.app) 构建的纯静态 ACG 作品知识库。
> 按「作品 → 章节」两层结构组织内容，支持多主题、三种布局模板、View Transitions 平滑切换、以及离线索引的站内全文搜索。

<div align="center">

![Astro](https://img.shields.io/badge/Astro-5.x-ff5d01?logo=astro)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?logo=typescript)
![MDX](https://img.shields.io/badge/MDX-Enabled-f9ac00)
![Pagefind](https://img.shields.io/badge/Pagefind-1.x-46a758)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

## ✨ 特性一览

| 特性 | 说明 |
| --- | --- |
| 📚 **按章节拆分** | 每个作品是一组 `.mdx` 文件；新增章节 = 新增一个文件 |
| 🎨 **三套主题** | `ocean`（蓝紫科幻）/ `crimson`（酒红）/ `amber`（琥珀金） |
| 📖 **三套布局** | `document`（三栏文档）/ `gallery`（网格图鉴）/ `timeline`（时间线） |
| 🔎 **离线索引搜索** | Pagefind 在构建时生成索引，前端即时匹配 |
| ✨ **SPA 级切换** | Astro View Transitions 在跨章节/跨作品间无缝过渡 |
| 🧩 **10+ MDX 组件** | `Callout`、`Card`、`HeroCard`、`TimelineNode`、`Quote`、`ImageGallery`、`InfoGrid`、`TagList`、`Aside`、`Divider` |
| 🖼 **响应式 AVIF/WebP 图片** | Astro `<Image>` 自动选择最佳格式 |
| 📑 **可折叠章节目录** | 每章的子大纲可展开/收起，章节目录支持"全部展开/收起" |
| 🎯 **滚动高亮（ScrollSpy）** | 滚动页面时右侧 TOC 自动高亮当前段落 |
| 📱 **响应式导航** | 窄屏设备上支持抽屉式侧边栏、固定返回按钮、弹出式本章目录 |
| 🎨 **统一滚动条样式** | 所有滚动条使用主题色，窄屏自动降级 |
| 🚀 **一键部署** | GitHub Pages + Actions，Push 到 `main` 即发布 |

## 📱 响应式导航说明

### 窄屏设备（≤720px）
- **顶部 action bar**：左侧为"← 返回作品首页"按钮；右侧为"☰ 章节"抽屉按钮（DocLayout 还有额外的"📑 目录"弹出层）
- **章节目录**：点击"☰ 章节"从左侧滑出，支持逐章展开子目录（h2/h3），也支持"全部展开/收起"
- **本章目录**：仅在 DocLayout 中可用，点击"📑 目录"弹出当前章节的大纲导航
- **返回按钮**：固定显示在 action bar 左侧，返回 `/{base}/works/<work>/`

### 平板（720–1100px）
- **左侧**：章节目录栏仍为三列布局，宽度缩减
- **右侧**：本章 TOC rail（DocLayout）

### 宽屏设备（＞1100px）
- **左侧**：sticky 章节目录栏，带滚动条美化，支持每章子目录展开/收起
- **右侧**（DocLayout 独有）：sticky 本章目录 rail，随页面滚动保持可见，配合 ScrollSpy 高亮

### 核心设计原则
1. **三栏 → 单栏 退化**：所有布局（Doc/Timeline/Gallery）共用同一套断点策略
2. **Action bar 固定**：窄屏顶部固定一个操作栏，避免用户在长文中迷失
3. **z-index 栈固定**：overlay(98) < side-nav(99) < action-bar(100) < TOC popover(101) < search dialog(200)
4. **单一 JS 脚本**：所有交互（侧栏开关、章节目录展开、TOC 高亮、Esc 关闭）集中在 `BaseLayout.astro` 中，避免重复

## 📁 目录结构

```
.
├── astro.config.mjs          # Astro 配置（site + base，支持 BASE_PATH env）
├── package.json
├── .github/workflows/deploy.yml   # GitHub Pages 自动部署
│
├── src/
│   ├── pages/                # 路由（自动生成静态页面）
│   │   ├── index.astro             # 首页（Hero + Features + Works 卡片）
│   │   ├── 404.astro               # 未找到
│   │   └── works/
│   │       ├── index.astro         # 作品列表
│   │       ├── [work]/index.astro  # 单个作品首页
│   │       └── [work]/[...slug].astro  # 章节详情（根据 frontmatter 选布局）
│   │
│   ├── layouts/              # 布局模板
│   │   ├── BaseLayout.astro        # 全局：header/footer/主题 + ViewTransitions + 所有交互脚本（侧栏/TOC/章节）
│   │   ├── DocLayout.astro         # 三栏文档（左章节目录 / 中正文 / 右 TOC rail）
│   │   ├── GalleryLayout.astro     # 响应式网格（图鉴型），也支持左侧章节目录
│   │   └── TimelineLayout.astro    # 时间线（剧情型），也支持左侧章节目录
│   │
│   ├── components/           # Astro 组件
│   │   ├── TableOfContents.astro   # 动态大纲目录（h2/h3/h4，可折叠，支持 rail/popover 两种模式）
│   │   ├── WorkNavigator.astro     # 作品切换 pill
│   │   ├── Pagination.astro        # 上/下章翻页
│   │   ├── SearchBox.astro         # 搜索按钮 + dialog 弹窗
│   │   ├── MdxImage.astro          # 基于 astro:assets 的响应式图片
│   │   ├── LazySection.astro       # 滚动进入才显现的容器
│   │   └── mdx/                    # ★ 白名单 MDX 组件（10 个）
│   │       ├── Callout.astro
│   │       ├── HeroCard.astro
│   │       ├── Card.astro
│   │       ├── ImageGallery.astro
│   │       ├── TimelineNode.astro
│   │       ├── InfoGrid.astro
│   │       ├── Quote.astro
│   │       ├── Divider.astro
│   │       ├── TagList.astro
│   │       └── Aside.astro
│   │
│   ├── utils/
│   │   ├── works.ts           # getWorks / getChapters / extract slugs
│   │   └── toc.ts             # slugify / buildToc / buildTocTree / ensureUnique / renderChaptersNav / renderTocForRail
│   │
│   ├── content/               # ★ 创作者编辑区（Content Collections）
│   │   ├── config.ts          # Zod Schema（章节 + 作品元数据）
│   │   ├── works/             # 作品 → 每份作品一份元数据 mdx
│   │   │   ├── dr-stone.mdx
│   │   │   └── maoyuu.mdx
│   │   └── chapters/          # 章节 → 按作品子目录组织
│   │       ├── dr-stone/
│   │       │   ├── chapter-01.mdx
│   │       │   └── chapter-02.mdx
│   │       └── maoyuu/
│   │           ├── chapter-01.mdx
│   │           └── chapter-02.mdx
│   │
│   └── styles/
│       └── theme.css          # 全局样式 + 三套主题（CSS 变量，含滚动条、选中文、kbd、dialog 等）
│
├── docs/
│   └── code-wiki.md          # 开发者文档（架构、数据层、布局层、组件 API、排错）
│
├── public/                    # 静态资源（可选）
├── src/assets/images/         # 图片资源（被 <Image> 处理）
└── dist/                      # 构建产物（构建时生成）
```

## 🚀 本地开发

### 前置
- Node.js ≥ 20
- npm ≥ 10

```bash
# 1. 安装依赖
npm install

# 2. 开发模式（HMR 热更新）
npm run dev
# 默认 → http://localhost:4321/Knowledge-based_ACG_Astro_Wiki/

# 3. 生产构建（同时生成 Pagefind 索引）
npm run build
# 产物位于 dist/

# 4. 本地预览生产构建（含搜索）
npm run preview
```

> 💡 **搜索功能只在 `npm run build` + `npm run preview` 后生效**，因为 Pagefind 索引是在 postbuild 阶段生成的。

## 📖 5 分钟：新增一个作品

假设你要添加「新世纪福音战士」→ slug 用 `evangelion`：

### 步骤 1：添加作品元数据

新建 **`src/content/works/evangelion.mdx`**：

```mdx
---
title: 新世纪福音战士
order: 3
summary: 公元 2015 年，巨大人形作战兵器 Evangelion 与使徒的战斗物语。
tags: ["机甲", "心理", "GAINAX"]
defaultThemePalette: "crimson"
defaultLayoutType: "document"
isDraft: false
---

## 作品简介

《新世纪福音战士》（新世紀エヴァンゲリオン）由 GAINAX 制作，庵野秀明担任总监督，
1995 年首播。故事围绕 14 岁的少年少女驾驶「EVA」对抗神秘敌人「使徒」展开。

## 世界设定

- **NERV**：直属联合国的特务机关
- **EVA**：泛用人型决战兵器
- **使徒**：来历不明的巨大生命体
```

### 步骤 2：添加章节

新建 **`src/content/chapters/evangelion/chapter-01.mdx`**：

```mdx
---
title: 第一章 · 使徒来袭
order: 1
layoutType: "document"
themePalette: "crimson"
tags: ["剧情", "第一话"]
summary: 第三新东京市遭遇第三使徒攻击，碇真嗣初次驾驶 EVA 初号机。
isDraft: false
---

## 关键事件

少年碇真嗣被父亲碇源堂召唤至第三新东京市，在迫不得已的情况下登上 **EVA 初号机**，
迎战第三使徒「Sachiel」。

<Quote cite="碇真嗣">
  不能逃避，不能逃避，不能逃避……
</Quote>

## 人物登场

<InfoGrid :items='[
  { "label": "碇真嗣", "value": "EVA 初号机驾驶员 / 第三适格者" },
  { "label": "绫波丽", "value": "EVA 零号机驾驶员 / 第一适格者" },
  { "label": "葛城美里", "value": "NERV 作战部课长 / 作战指挥" }
]' />

## 氛围

<Callout type="warning" title="心理描写重">
  《EVA》的战斗只是外壳，真正的主题是角色内心的补完与沟通。
  建议关注真嗣面对压力时的应对方式。
</Callout>
```

> **关于章节目录**：章节正文中的 `## / ###` 标题会被自动提取为子目录，出现在：
> - 作品首页的章节目录中（窄屏需点击"全部展开"查看）
> - DocLayout 右侧的本章目录 rail（宽屏）
> - DocLayout 窄屏的"📑 目录"弹出层

按需添加更多章节（`chapter-02.mdx`、`chapter-03.mdx` …）。

### 步骤 3：确认

```bash
npm run build      # Schema 校验 + 生成路由
```

- 缺少 `title` / `order` 等必填字段 → 构建**会失败**（fail-fast）
- `isDraft: true` 的章节 → 生产构建中**不会被渲染**
- 浏览 `/works/evangelion/` 查看作品首页

就这么多！你不需要修改任何代码。

## ⚙️ 配置项参考（Frontmatter）

### 作品级 (在 `src/content/works/<slug>.mdx`)

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | ✅ | 作品显示名 |
| `order` | number | ➖ | 在作品列表中的排序权重（默认 0） |
| `summary` | string | ➖ | 用于作品卡片的简介 |
| `tags` | string[] | ➖ | 标签列表 |
| `cover` | string | ➖ | 封面路径（`src/assets/…`） |
| `defaultThemePalette` | `ocean \| crimson \| amber` | ➖ | 章节默认主题（默认 `ocean`） |
| `defaultLayoutType` | `document \| gallery \| timeline` | ➖ | 章节默认布局（默认 `document`） |
| `isDraft` | boolean | ➖ | `true` 时不渲染 |

### 章节级 (在 `src/content/chapters/<work>/<slug>.mdx`)

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | ✅ | 章节标题 |
| `order` | number | ✅ | 作品内的章节序号（用于翻页与排序） |
| `layoutType` | 同作品 | ➖ | **覆盖**作品默认布局 |
| `themePalette` | 同作品 | ➖ | **覆盖**作品默认主题 |
| `tags` | string[] | ➖ | 章节标签 |
| `summary` | string | ➖ | 章节简介 |
| `isDraft` | boolean | ➖ | `true` 时不渲染 |

**布局类型说明**：

| layoutType | 适用场景 | 章节目录 | 本章 TOC |
| --- | --- | --- | --- |
| `document` | 剧情/设定类长文 | ✅ 左栏 | ✅ 右栏 rail + 窄屏弹出层 |
| `timeline` | 编年史/事件列表 | ✅ 左栏 | ❌ |
| `gallery` | 角色图鉴/设定图 | ✅ 左栏 | ❌ |

## 🎨 MDX 自定义组件（白名单）

在章节内容中可直接使用这些组件。所有组件都支持嵌套 Markdown。

### 1. `<Callout>`

```mdx
<Callout type="info" title="提示">这是一条补充信息。</Callout>
<Callout type="warning" title="警告">剧透内容。</Callout>
<Callout type="success">示例通过。</Callout>
<Callout type="note" title="作者按">个人笔记。</Callout>
```

### 2. `<HeroCard>`

```mdx
<HeroCard title="核心设定" icon="🗝️">
  A.T. Field 的本质是心灵的屏障。
</HeroCard>
```

### 3. `<Card>`

```mdx
<Card title="出场作品" subtitle="TV 26 话 + 旧剧场版 + 新剧场版 4 部">
  - TV (1995)
  - 死与新生 (1997)
  - Air/真心为你 (1997)
  - 新剧场版 (序·破·Q·终, 2007–2021)
</Card>
```

### 4. `<TimelineNode>`

```mdx
<TimelineNode year="2000" title="第二次冲击">
  南极出现巨大光之巨人，造成全球规模的灾难。
</TimelineNode>
<TimelineNode year="2015" title="使徒来袭">
  第三使徒出现在第三新东京市，EVA 初号机首次实战。
</TimelineNode>
```

### 5. `<Quote>`

```mdx
<Quote cite="碇真嗣">不能逃避，不能逃避，不能逃避……</Quote>
```

### 6. `<InfoGrid>`

```mdx
<InfoGrid :items='[
  { "label": "出身", "value": "新京都" },
  { "label": "年龄", "value": "14" },
  { "label": "驾驶机体", "value": "EVA 初号机" }
]' />
```

### 7. `<TagList>`

```mdx
<TagList heading="标签" items={['机甲', '心理', 'GAINAX']} />
```

### 8. `<ImageGallery>`

```mdx
<ImageGallery columns={3}>
  <img src="./images/sample-1.jpg" alt="场景一" />
  <img src="./images/sample-2.jpg" alt="场景二" />
  <img src="./images/sample-3.jpg" alt="场景三" />
</ImageGallery>
```

> 推荐使用 `import` 的方式引用 `src/assets/images/` 下的图片以获得自动 AVIF/WebP。

### 9. `<Divider>`

```mdx
<Divider text="间章" />
```

### 10. `<Aside>`

```mdx
<Aside title="小知识">
  A.T. Field 的全称是「Absolute Terror Field」。
</Aside>
```

## 🔎 搜索（Pagefind）

- 构建命令执行后，`npm run postbuild` 会自动执行 `pagefind --site dist`
- 生成的索引位于 `dist/pagefind/`
- 点击站点顶栏的 🔍 搜索按钮打开弹窗
- 支持 Ctrl/⌘ + K 快捷键唤起搜索框

## 🌐 部署到 GitHub Pages

仓库已预置 `.github/workflows/deploy.yml`。

### 步骤

1. 新建 GitHub 仓库并 Push 代码到 `main` 分支
2. 在 GitHub 仓库 → **Settings → Pages**：
   - **Source** 选择 **GitHub Actions**
3. 等待 Actions 自动执行 `build` → `upload-pages-artifact` → `deploy-pages`
4. 发布完成后即可访问 `https://<your-name>.github.io/<repo-name>/`

### 关于 `base` 路径

- `astro.config.mjs` 默认 `base = '/Knowledge-based_ACG_Astro_Wiki/'`
- CI 环境会**自动覆盖**为 `/<repo-name>/`
- 如需本地指定其他路径：
  ```bash
  BASE_PATH=/my-wiki/ npm run build
  ```

## 🏗 架构设计

详见 [`docs/code-wiki.md`](docs/code-wiki.md)：

- 数据层与视图层分离（Content Collections → Astro 布局）
- Zod Schema 与 fail-fast 构建
- CSS 变量驱动的多主题系统（含滚动条、kbd、dialog 等统一变量）
- TOC ScrollSpy 的 IntersectionObserver 生命周期
- View Transitions 在 Astro 中的使用模式
- 响应式断点与 z-index 栈
- 常见部署错误排查

## 📜 License

MIT — 欢迎复刻为你自己的知识库。
