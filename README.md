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
| 📱 **响应式导航** | 窄屏设备上支持抽屉式侧边栏、固定返回按钮、展开/收起章节目录 |
| 🚀 **一键部署** | GitHub Pages + Actions，Push 到 `main` 即发布 |

## 📱 响应式导航说明

### 窄屏设备（≤720px）
- **左上角**：固定显示"返回"作品首页按钮
- **左侧**：抽屉式章节目录，点击展开按钮显示完整章节列表
- **右上角**："本章目录"按钮，点击展开当前章节的大纲导航

### 宽屏设备（＞720px）
- **左侧**：固定的章节目录栏（可收起/展开）
- **右侧**：sticky 定位的本章目录，随页面滚动保持可见

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
│   │   ├── BaseLayout.astro        # 全局：header/footer/主题 + ViewTransitions
│   │   ├── DocLayout.astro         # 三栏文档（左章节目录 / 中正文 / 右 TOC）
│   │   ├── GalleryLayout.astro     # 响应式网格（图鉴型）
│   │   └── TimelineLayout.astro    # 时间线（剧情型）
│   │
│   ├── components/           # Astro 组件
│   │   ├── TableOfContents.astro   # 动态大纲目录（h2/h3/h4）
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
│   │   └── toc.ts             # slugify / buildToc
│   │
│   ├── content/               # ★ 创作者编辑区（Content Collections）
│   │   ├── config.ts          # Zod Schema（章节 + 作品元数据）
│   │   ├── works/             # 作品 → 每份作品一份元数据 mdx
│   │   │   ├── dr-stone.mdx
│   │   │   └── maoyuu.mdx
│   │   └── chapters/          # 章节 → 按作品子目录组织
│   │       ├── dr-stone/
│   │       │   ├── chapter-01.mdx
│   │       │   ├── chapter-02.mdx
│   │       │   └── chapter-03.mdx
│   │       └── maoyuu/
│   │           ├── chapter-01.mdx
│   │           └── chapter-02.mdx
│   │
│   └── styles/
│       └── theme.css          # 全局样式 + 三套主题（CSS 变量）
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
- CSS 变量驱动的多主题系统
- TOC ScrollSpy 的 IntersectionObserver 生命周期
- View Transitions 在 Astro 中的使用模式
- 常见部署错误排查

## 📜 License

MIT — 欢迎复刻为你自己的知识库。
