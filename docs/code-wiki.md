# ACG 知识库 — Code Wiki

> 本项目是基于动画、漫画、游戏作品的知识整理与科普静态站点。
> 本文档从**工程与代码**角度系统梳理项目架构、模块职责、关键实现、依赖关系与运行方式，
> 供维护者、贡献者与二次开发者参考。

---

## 1. 项目概览

| 项目 | 说明 |
| --- | --- |
| 项目名称 | ACG 知识库（Knowledge-based ACG Works） |
| 项目类型 | 纯静态 HTML / CSS / JavaScript 内容站 |
| 构建方式 | **零构建、零打包依赖** — 源码即产物 |
| 运行环境 | 任意静态服务器 / GitHub Pages / 直接双击 HTML |
| JavaScript 语法 | ES5（兼容 `file://` 协议直接打开） |
| CSS 方案 | CSS 变量驱动的主题化 + BEM 风格类名约定 |
| 托管方案 | GitHub Pages |
| 持续部署 | GitHub Actions（`.github/workflows/deploy.yml`） |
| 代码规范 | EditorConfig + Prettier（`.prettierrc`） |
| 开源协议 | MIT |

### 1.1 代码仓库目标

- 将 ACG 作品中的**非虚构知识**（科学、政治经济学、料理文化等）以结构化 HTML 页面呈现。
- 保持**内容层 / 骨架层 / 主题层 / 脚本层**的严格分离，降低维护成本。
- 提供一个**零构建**的静态站框架，使非前端背景的贡献者也能轻松新增作品页面。

### 1.2 当前已收录子项目

| 子项目 | 目录 | 页面数量 | 主题色 |
| --- | --- | --- | --- |
| 《石纪元》科学知识手册 | `content/dr-stone-science/` | 10 个页面（封面 + 8 章 + 附录） | 暗色科技（深蓝绿） |
| 《魔王勇者》政治经济学手册 | `content/maoyuu-political-economy/` | 9 个页面（概览 + 5 卷 + 外传 + 分析） | 酒红学术 |
| 异世界流浪美食家料理图鉴 | `content/tondemo-skill-food/` | 3 个页面（封面 + 两季） | 暖色料理 |
| 《食戟之灵》料理内容文档 | `content/shokugeki-no-soma/` | 11 个页面（封面 + 10 篇章） | 白纸料理 |

---

## 2. 整体架构

本项目采用**内容层 / 骨架层 / 主题层 / 脚本层**四层分离的静态页面架构：

```
┌──────────────────────────────────────────────────────┐
│                  内容层 Content Layer                 │
│  index.html, content/*/index.html, content/*/*.html  │
│  → 仅写语义化 HTML（section / h2 / h3 / article ...） │
│  → 不允许写 <style>、<script> 或内联样式               │
└──────────────────────────┬───────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   骨架层 styles/        主题层 styles/      脚本层 scripts/
   core.css            themes/*.css        navigation.js
   ├─ Reset / Base      ├─ CSS 变量换肤     ├─ 导航切换
   ├─ Container / Hero  ├─ 项目专属组件样式 ├─ 折叠展开
   ├─ Card / Tag        └─ 项目专属响应式   ├─ 目录高亮
   ├─ Sidebar / TOC                         ├─ 筛选过滤
   ├─ Site-header / Footer                   ├─ 平滑滚动
   ├─ Back-to-top                             └─ 自动生成 TOC
   ├─ 响应式断点
   └─ 打印样式
```

### 2.1 架构原则

1. **内容与表现分离** — HTML 只负责语义，所有视觉样式在 CSS 中。
2. **通用与专用分离** — 全站通用组件（card / tag / hero / site-header 等）进入 `core.css`，项目专属组件（dish-card / toc-tree / arc-grid 等）进入各主题 CSS。
3. **零构建原则** — 不使用任何打包工具，HTML 以相对路径引用 CSS 与 JS。
4. **主题变量化** — 每个子项目的外观由覆盖 `:root` 中的 CSS 变量完成换肤。
5. **渐进增强** — JS 不可用时页面依然可读；JS 仅负责**交互增强**。

---

## 3. 目录结构

```
/workspace
├── index.html                  # 站点首页（项目卡片入口）
├── .editorconfig              # 跨编辑器一致缩进 / 换行 / 编码
├── .prettierrc                # Prettier 代码格式化规则
├── .gitignore                 # 忽略 IDE / 临时 / 依赖 / 构建产物
├── .nojekyll                  # 告知 GitHub Pages 不要走 Jekyll 管线
├── LICENSE                    # MIT 协议
├── jsconfig.json              # VS Code 下 JS 路径别名（@/* → ./*）
├── README.md                  # 项目说明（面向用户 + 面向贡献者）
│
├── assets/                    # 静态资源
│   ├── fonts/
│   │   └── ArsenalSC-Regular.ttf        # 本地字体（兜底用）
│   └── images/
│       ├── dr-stone-science/            # 《石纪元》图片
│       ├── maoyuu-political-economy/    # 《魔王勇者》图片
│       ├── shokugeki-no-soma/           # 《食戟之灵》图片
│       └── tondemo-skill-food/          # 流浪美食家图片
│
├── content/                   # 内容页面（语义 HTML，不写 <style> / <script>）
│   ├── dr-stone-science/
│   │   ├── index.html                     # 封面 / 目录
│   │   ├── ch1-overview.html              # 第一章
│   │   ├── ch2-primitive.html             # 第二章
│   │   ├── ch3-kingdom.html               # 第三章
│   │   ├── ch4-wars.html                  # 第四章
│   │   ├── ch5-voyage.html                # 第五章
│   │   ├── ch6-treasure.html              # 第六章
│   │   ├── ch7-newworld.html              # 第七章
│   │   ├── ch8-space.html                 # 第八章
│   │   └── appendix.html                  # 附录
│   │
│   ├── maoyuu-political-economy/
│   │   ├── index.html                     # 首页 / 世界观 / 核心概念
│   │   ├── story-synopsis.html            # 五卷故事梗概
│   │   ├── volume-1.html .. volume-5.html # 第一至第五卷详解
│   │   ├── side-stories.html              # 外传三卷
│   │   └── narrative-analysis.html        # 整体叙事脉络分析
│   │
│   ├── shokugeki-no-soma/
│   │   ├── index.html                     # 封面 / 作品简介
│   │   ├── arc-01-enrollment.html         # 第 1 篇章
│   │   ├── arc-02-training.html           # 第 2 篇章
│   │   ├── arc-03-autumn-election.html    # 第 3 篇章
│   │   ├── arc-04-kuga-shokugeki.html     # 第 4 篇章
│   │   ├── arc-05-stagiaire.html          # 第 5 篇章
│   │   ├── arc-06-moon-festival.html      # 第 6 篇章
│   │   ├── arc-07-train.html              # 第 7 篇章
│   │   ├── arc-08-regiment.html           # 第 8 篇章
│   │   ├── arc-09-blue.html               # 第 9 篇章
│   │   └── arc-10-dessert.html            # 第 10 篇章
│   │
│   └── tondemo-skill-food/
│       ├── index.html                     # 封面 / 简介 / 食材表
│       ├── season1.html                   # 第一季（12 话）
│       └── season2.html                   # 第二季（12 话）
│
├── scripts/
│   └── navigation.js          # 全站通用交互脚本（唯一 JS 文件）
│
├── styles/
│   ├── core.css               # 全站骨架样式（reset + 布局 + 通用组件）
│   └── themes/
│       ├── home.css                       # 首页主题（深色）
│       ├── dr-stone-science.css           # 石纪元主题
│       ├── maoyuu-political-economy.css   # 魔王勇者主题
│       ├── tondemo-skill-food.css         # 流浪美食家主题
│       └── shokugeki-no-soma.css          # 食戟之灵主题
│
└── .github/
    └── workflows/
        └── deploy.yml           # GitHub Actions Pages 自动部署
```

---

## 4. 模块职责详解

### 4.1 入口页面：`index.html`

- **定位**：全站首页，用户进入四个子项目的入口。
- **结构**：
  - `.site-header` — 顶部导航栏（Logo + 四个作品链接）
  - `.hero` — 大标题与项目一句话介绍
  - `.projects-grid` — 4 张 `.project-card` 卡片，点击跳转各子项目首页
  - `.site-footer` — 底部版权与协议声明
- **引用**：
  - `styles/core.css`（骨架）
  - `styles/themes/home.css`（首页专属主题，深色背景 + 强调色 `#e94560`）
  - `scripts/navigation.js`（交互增强）

### 4.2 内容层：`content/*/*.html`

每个子项目目录都遵循统一约定：

1. 必有 `index.html`，作为该子项目的**封面页 + 目录**。
2. 章节页以语义化命名（`ch` / `volume-` / `arc-` / `season` + `.html`）。
3. 所有章节页都引用 `styles/core.css` + `styles/themes/<project>.css` + `scripts/navigation.js`。
4. 页面内部包含统一的 **site-header / site-footer / main-content** 三段式结构。
5. **禁止**在内容 HTML 中写任何 `<style>` 或 `onclick` 外的脚本逻辑。
6. 若项目需要筛选 / 自动目录 / 料理卡片等项目专属结构，应在**主题 CSS** 或**通用 JS** 中完成。

### 4.3 骨架层：`styles/core.css`

这是全站**唯一**的共享样式来源，内容分为若干区块（按注释编号）：

| 区块 | 职责 | 主要类 / 变量 |
| --- | --- | --- |
| 1. Google Fonts CDN | 字体引入 | `@import` Lora, Work Sans, Noto Serif SC |
| 2. CSS Variables（默认主题） | 默认颜色 / 字体 / 尺寸变量 | `--bg, --ink, --accent, --font-heading, --content-width` 等 |
| 3. Reset & Base | 统一盒模型、行高、滚动行为 | `*, html, body, img` |
| 4. Typography | 标题 / 段落 / 列表 / blockquote / code | `h1-h6, p, ul, ol, blockquote, code` |
| 5. Layout & Container | 栅格容器与最大宽度 | `.container, .main-content` |
| 6. Components — Hero | 首页 / 封面大标题组件 | `.hero, .hero-content, .subtitle` |
| 7. Components — Card / Tag / Filter | 通用卡片、标签、筛选栏 | `.card, .tag, .filter-bar, .filter-btn` |
| 8. Components — Site Header / Nav | 顶部导航与汉堡菜单 | `.site-header, .site-nav, .nav-toggle, .site-logo` |
| 9. Components — Sidebar / TOC | 左侧目录组件（两类：`.sidebar-toc` 与 `.sidebar`） | `.sidebar-toc, .sidebar, .sidebar-overlay, .hamburger` |
| 10. Components — Section Title / TOC List | 章节标题与目录列表 | `.section-title, .title-en, .toc-list, .toc-sub` |
| 11. Components — Collapsible | 可折叠内容块 | `.collapsible-toggle, .collapsible, h3[data-collapsible]` |
| 12. Components — Back-to-top | 滚动回顶按钮 | `.back-to-top` |
| 13. Components — Site Footer | 底部 | `.site-footer, .copyright` |
| 14. Utilities | 通用工具类（间距 / 对齐 / 文本色） | `.text-muted, .text-center, .mt-*` 等 |
| 15. Responsive | 响应式断点（768px / 1024px） | `@media (max-width: 768px)` |
| 16. Print | 打印样式 | `@media print` |

**为什么把通用组件放在 core.css 而不是主题 CSS 中？**
- 为了避免不同主题中出现重复的布局代码；项目专属组件（例如 `dish-card` / `toc-tree` / `arc-grid`）则放到各自的主题 CSS。

### 4.4 主题层：`styles/themes/*.css`

每个主题 CSS 完成两件事：

1. **覆盖 `:root` CSS 变量**（换肤）— 这是主题化的关键。
2. **定义项目专属组件样式**（仅在该项目出现的组件，例如 `dish-card` / `arc-grid` / `toc-tree` 等）。

**主题 CSS 必须至少包含以下变量（规范约定）：**

```css
:root {
  --bg:             /* 页面主体背景 */
  --bg2:            /* 次要背景（卡片、表格头） */
  --ink:            /* 正文文字颜色 */
  --muted:          /* 次要文字 / 辅助说明 */
  --rule:           /* 边框 / 分割线 */
  --accent:         /* 主题色（链接、按钮、强调） */
  --accent2:        /* 第二强调色（徽章、次要强调） */
  --ink-on-accent:  /* 放在 accent 背景上的文字颜色（通常为白色） */

  --font-heading:   /* 标题字体 */
  --font-body:      /* 正文字体 */
  --content-width:  /* 正文最大宽度（例如 1080px / 1200px） */
}
```

**各主题风格对照表**：

| 主题文件 | 适用页面 | 风格关键词 | 主 accent |
| --- | --- | --- | --- |
| `home.css` | `index.html` | 深色科技 / 作品集入口 | `#e94560` |
| `dr-stone-science.css` | `content/dr-stone-science/*` | 深蓝绿 / 实验室感 | `#00b4d8` |
| `maoyuu-political-economy.css` | `content/maoyuu-political-economy/*` | 酒红 / 学术出版物 | `#b33a3a` |
| `tondemo-skill-food.css` | `content/tondemo-skill-food/*` | 暖色纸张 / 料理书 | `#e07a5f` |
| `shokugeki-no-soma.css` | `content/shokugeki-no-soma/*` | 白纸 / 经典排版 | `#c0392b` |

### 4.5 脚本层：`scripts/navigation.js`

这是全站**唯一**的 JS 文件，采用 IIFE 封装，以 ES5 语法书写（兼容 `file://` 直接打开）。所有函数遵循"元素不存在则静默退出"的原则，确保无关页面不会报 `null` 错误。

#### 初始化入口

在 `DOMContentLoaded` 事件中依次调用：

```
initNavToggle()
initSidebarToggles()
initCollapsibles()
initBackToTop()
initSideTocHighlight()
initSmoothScroll()
initCuisineFilter()
initAutoToc()
initTocTreeExpand()
initTocTreeHighlight()
```

#### 各函数职责

| 函数 | 触发元素 / 数据属性 | 功能 |
| --- | --- | --- |
| `initNavToggle()` | `.nav-toggle` ↔ `.site-nav` | 响应式汉堡菜单展开收起 |
| `initSidebarToggles()` | `[data-sidebar-toggle]`, `.hamburger`, `.sidebar`, `.sidebar-overlay` | 左侧目录侧栏的通用开关 |
| `initCollapsibles()` | `.collapsible-toggle`, `h3[data-collapsible]` | 点击展开/收起内容块 |
| `initBackToTop()` | `.back-to-top` | 滚动超过 400px 显示按钮，点击平滑回顶 |
| `initSideTocHighlight()` | `.side-toc / .sidebar-toc a[href^="#"]` | 滚动时高亮当前章节链接 |
| `initSmoothScroll()` | 所有 `a[href^="#"]` | 对站内锚点应用平滑滚动 |
| `initCuisineFilter()` | `.filter-btn[data-filter]` ↔ `.dish-card[data-cuisine]` | 料理分类筛选（流浪美食家 / 食戟之灵） |
| `initAutoToc()` | `#tocTree` + `#mainContent` | 依据 `section[id]` 和 `h3[id]` 动态生成左侧目录树（魔王勇者专用） |
| `initTocTreeExpand()` | `.toc-toggle` ↔ `.toc-children` | toc-tree 的逐级展开折叠 |
| `initTocTreeHighlight()` | `#tocTree .toc-node[data-target]` | toc-tree 版本的滚动高亮 |

#### 对外暴露的全局函数

为方便 HTML 中通过 `onclick` 调用少量"整页操作"，脚本在 `window` 上挂载了三个全局函数：

| 函数 | 效果 |
| --- | --- |
| `window.expandAll()` | 展开所有 `.toc-children`、`.collapsible`、`h3` 折叠块 |
| `window.collapseAll()` | 收起所有上述块 |
| `window.toggleSection(id, headingEl)` | 切换单个 `.collapsible` 的展开状态 |

#### 技术要点

- **无框架依赖** — 纯原生 DOM API（`querySelector` / `querySelectorAll` / `addEventListener` / `classList` / `scrollIntoView`）。
- **防御性编程** — 每个 `init*` 函数第一行检查目标元素是否存在，不存在直接 `return`。
- **性能优化** — `initTocTreeHighlight()` 使用 `requestAnimationFrame` 节流 `scroll` 事件。
- **IIFE 封装** — 所有函数声明在 `(function(){ ... })();` 内部，除三个 `window.*` 方法外不污染全局。
- **兼容性** — 刻意避免 ES6+ 语法（无 `const` / `let` / 箭头函数 / 模板字符串），以保证在 `file://` 协议下直接双击 HTML 可用，避免受浏览器 file 协议的 CSP 限制。

---

## 5. 关键类 / 数据属性 / CSS 变量说明

### 5.1 关键类名

| 类名 | 归属 | 作用 |
| --- | --- | --- |
| `.site-header` / `.site-footer` | core.css | 站点顶部 / 底部 |
| `.site-logo` / `.site-nav` / `.nav-toggle` | core.css | 顶部导航与响应式菜单按钮 |
| `.hero` / `.hero-content` / `.subtitle` | core.css | 页面封面大标题组件 |
| `.container` | core.css | 受 `--content-width` 约束的内容容器 |
| `.main-content` | core.css / 主题 | 正文区 wrapper |
| `.project-card` | home.css | 首页 4 张项目入口卡 |
| `.sidebar-toc` | core.css | 石纪元 / 食戟之灵 风格的左侧目录 |
| `.sidebar` / `.sidebar-overlay` / `.hamburger` | core.css + 主题 CSS | 魔王勇者 / 流浪美食家 风格的左侧栏 |
| `.toc-list` / `.toc-sub` | core.css | 章节目录列表与副标题 |
| `.section-title` / `.title-en` | core.css | 章节标题组件 |
| `.collapsible-toggle` / `.collapsible` | core.css | 可折叠内容块 |
| `.back-to-top` | core.css | 滚动回顶按钮 |
| `.filter-btn` / `.dish-card[data-cuisine]` | core.css + 主题 CSS | 料理分类筛选按钮 / 卡片 |
| `.toc-tree` / `.toc-children` / `.toc-toggle` / `.toc-node` | maoyuu-political-economy.css + navigation.js | 魔王勇者的树形目录组件 |
| `.toc-toggle.leaf` | maoyuu-political-economy.css | 叶子节点标识，点击不会触发展开 |
| `expanded` / `open` / `active` / `visible` | core.css + 各主题 CSS | 状态类（展开 / 打开 / 高亮 / 可见） |

### 5.2 关键数据属性

| 属性 | 位置 | 作用 |
| --- | --- | --- |
| `data-sidebar-toggle` | `button` 或任意可点击元素 | 触发侧栏开关 |
| `data-target` | `.toc-node` / `.sidebar-toggle` | 目标 `id`；平滑滚动锚点 |
| `data-filter` | `.filter-btn` | 筛选条件（例如 `all` / `meat` / `dessert`） |
| `data-cuisine` | `.dish-card` | 被筛选的目标分类 |
| `data-collapsible` | `h3` | 声明该标题为可折叠区块标题 |

### 5.3 关键 CSS 变量（所有主题必选）

```
--bg, --bg2, --ink, --muted, --rule,
--accent, --accent2, --ink-on-accent,
--font-heading, --font-body, --content-width
```

**仅存在于 `core.css`**（非主题必需但主题可覆盖）：

```
--card-bg, --card-radius, --section-gap,
--shadow-sm, --shadow-md, --shadow-lg,
--trans-quick, --trans, --trans-slow,
--font-mono
```

---

## 6. 项目依赖关系

### 6.1 代码依赖图

```
index.html
  ├─ styles/core.css                    ← 全站骨架
  ├─ styles/themes/home.css             ← 首页主题
  └─ scripts/navigation.js              ← 全站交互

content/dr-stone-science/*.html
  ├─ styles/core.css
  ├─ styles/themes/dr-stone-science.css
  ├─ scripts/navigation.js
  └─ assets/images/dr-stone-science/*

content/maoyuu-political-economy/*.html
  ├─ styles/core.css
  ├─ styles/themes/maoyuu-political-economy.css
  ├─ scripts/navigation.js
  └─ assets/images/maoyuu-political-economy/*

content/tondemo-skill-food/*.html
  ├─ styles/core.css
  ├─ styles/themes/tondemo-skill-food.css
  ├─ scripts/navigation.js
  └─ assets/images/tondemo-skill-food/*

content/shokugeki-no-soma/*.html
  ├─ styles/core.css
  ├─ styles/themes/shokugeki-no-soma.css
  ├─ scripts/navigation.js
  └─ assets/images/shokugeki-no-soma/*
```

**核心不变量**：所有 HTML 都只引用 `core.css` + `themes/<project>.css` + `navigation.js`，没有项目私有的 JS 文件。

### 6.2 外部 CDN 依赖

| 依赖 | 引入位置 | 用途 | 版本 / 策略 |
| --- | --- | --- | --- |
| Google Fonts: Lora / Work Sans / Noto Serif SC | `styles/core.css` `@import` / `index.html` `<link>` | 正文与标题字体 | 浏览器按需加载 |
| Google Fonts: Inter | `index.html` `<link>` | 首页正文字体（与作品页区分） | 仅首页使用 |
| ECharts | 具体页面内的 `<script>`（按需） | 绘制数据可视化（热力图、饼图） | 按需加载，无全局依赖 |
| Mermaid | 具体页面内的 `<script>`（按需） | 绘制流程图 / 科技树 | 按需加载，无全局依赖 |

> 项目**不**在 `core.css` / `navigation.js` 层面引入 ECharts / Mermaid；仅在具体需要可视化的作品页面内按需引入，保持零全局负担。

### 6.3 本地依赖

- `assets/fonts/ArsenalSC-Regular.ttf` — 本地字体，作为 Google Fonts 加载失败的兜底（仅部分作品页使用）。

### 6.4 构建 / 工具链依赖（开发期使用，不影响运行）

| 工具 | 配置文件 | 用途 |
| --- | --- | --- |
| EditorConfig | `.editorconfig` | 跨编辑器统一缩进（2 空格）、换行（LF）、编码（UTF-8）、去掉行尾空格 |
| Prettier | `.prettierrc` | 统一 HTML / CSS / JS / JSON / YAML 格式（单引号、100 字符换行、LF、`arrowParens: avoid`、`htmlWhitespaceSensitivity: css`） |
| VS Code jsconfig | `jsconfig.json` | `@/*` 路径映射；标记目标 ES6；包含 `scripts/**/*.js` 与 `content/**/*.js` |
| Git | `.gitignore` | 忽略 IDE（`.trae/`, `.vscode/`, `.idea/`）、临时文件、`node_modules/`、构建产物、环境变量 |

---

## 7. 运行方式

### 7.1 方式 A：直接双击 HTML

所有页面均为纯静态内容，可直接：

```
双击 index.html → 在浏览器中查看
```

> 注意：`navigation.js` 使用 ES5 语法，部分浏览器的 `file://` 协议对 `@import` CSS / `<script src>` 有限制，但本项目均为相对路径的本地文件，因此不会触发跨域问题。若页面大量图片 / Google Fonts 需要联网，请确保网络畅通。

### 7.2 方式 B：Python 内置 HTTP 服务器（推荐本地开发）

```bash
cd /workspace
python3 -m http.server 8000
# 或 Windows: python -m http.server 8000
```

浏览器访问 `http://localhost:8000`。

### 7.3 方式 C：Node.js `serve`

```bash
npx serve .
```

### 7.4 方式 D：GitHub Pages（生产部署）

项目根目录存在 `.nojekyll` 文件，告知 GitHub Pages **不要**进行 Jekyll 构建（避免以 `_` 开头的目录被忽略）。

推送至 `main` / `master` 分支后，`.github/workflows/deploy.yml` 会自动触发部署，具体流程见下一节。

---

## 8. 部署流程（GitHub Actions）

### 8.1 Workflow 文件位置

`.github/workflows/deploy.yml`

### 8.2 触发条件

```yaml
on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:        # 支持 GitHub 页面手动触发
```

### 8.3 权限声明

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
```

`concurrency.group: "pages"` 保证同一分支的多次 push 不会并行触发部署。

### 8.4 作业步骤（单 job：`deploy`）

```
runs-on: ubuntu-latest
 1. actions/checkout@v5             — 拉取仓库（整个项目即产物）
 2. actions/configure-pages@v6      — 配置 Pages 环境（OIDC token / base URL）
 3. actions/upload-pages-artifact@v5 — 上传整个仓库作为 Pages artifact（path: '.'）
 4. actions/deploy-pages@v5         — 将 artifact 部署到 GitHub Pages
```

### 8.5 启用 Pages 的前置条件（一次性操作）

1. 仓库 Settings → Pages → Source 选择 **GitHub Actions**。
2. 推送至 `main` / `master`，或在 Actions 页面手动 Run workflow。
3. 部署完成后访问 `https://<username>.github.io/<repo>/`。

### 8.6 `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`

Workflow 显式设置了 `env.FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`，用于在 GitHub Actions runner 中以 Node 24 运行 `actions/*` 相关 JS Action，避免 runner 默认 Node 版本过低的兼容问题。

---

## 9. 新增作品页（标准流程）

### 9.1 目录结构

```
content/my-new-work/
  ├─ index.html            ← 封面 + 目录
  ├─ chapter-01.html       ← 章节页（按需创建）
  └─ chapter-02.html       ← 更多章节 ...

styles/themes/
  └─ my-new-work.css       ← 项目主题

assets/images/my-new-work/
  └─ ... (图片资源)
```

### 9.2 最小 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>XXX — ACG 知识库</title>
  <link rel="stylesheet" href="../../styles/core.css">
  <link rel="stylesheet" href="../../styles/themes/my-new-work.css">
  <script defer src="../../scripts/navigation.js"></script>
</head>
<body>

  <header class="site-header">
    <div class="container">
      <a href="../../index.html" class="site-logo">
        <span class="logo-icon">📖</span>
        <span>XXX 手册</span>
      </a>
      <button class="nav-toggle" aria-label="菜单">☰</button>
      <nav class="site-nav">
        <a href="../../index.html">← 返回首页</a>
        <a href="../dr-stone-science/index.html">石纪元</a>
        <a href="../maoyuu-political-economy/index.html">魔王勇者</a>
        <a href="../tondemo-skill-food/index.html">流浪美食家</a>
        <a href="../shokugeki-no-soma/index.html">食戟之灵</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <section class="hero">
      <div class="container">
        <h1>XXX</h1>
        <p class="subtitle">一句话介绍这个作品</p>
      </div>
    </section>

    <section class="container">
      <h2 class="section-title">第一章 <span class="title-en">Chapter 1</span></h2>
      <p>你的正文内容 ...</p>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>XXX · ACG 知识库</p>
      <p class="copyright">原作：XXX。本站内容 MIT 开源，图片素材归原作者所有。</p>
    </div>
  </footer>

</body>
</html>
```

### 9.3 最小 CSS 模板

```css
:root {
  --bg:            #ffffff;
  --bg2:           #f5f5f5;
  --ink:           #1a1a1a;
  --muted:         #777777;
  --rule:          #e5e5e5;
  --accent:        #c0392b;
  --accent2:       #f39c12;
  --ink-on-accent: #ffffff;

  --font-heading:  'Lora', 'Noto Serif SC', Georgia, serif;
  --font-body:     'Work Sans', 'Noto Sans SC', 'PingFang SC',
                   'Microsoft YaHei', sans-serif;
  --content-width: 1080px;
}

/* 项目专属组件样式（可选） */
.my-special-card { ... }
```

### 9.4 首页入口

在 `index.html` 的 `.projects-grid` 中追加一张新卡片：

```html
<a href="./content/my-new-work/index.html" class="project-card">
  <div class="project-icon">🆕</div>
  <h2>新作品</h2>
  <p>一句话介绍。</p>
  <div class="project-meta">
    <span class="project-tag">分类标签</span>
    <span class="project-arrow">→</span>
  </div>
</a>
```

### 9.5 校验与提交

```bash
python3 -m http.server 8000
# 浏览器检查新页布局 / 图片 / 链接正常
git add .
git commit -m "feat: add my-new-work"
git push origin main
# 等待 GitHub Actions 部署完成
```

---

## 10. 代码规范与约束

### 10.1 内容 HTML 规范

- 使用 UTF-8。
- 页面内**不**写 `<style>` 标签、**不**写内联脚本。
- `<script defer src="../../scripts/navigation.js">` — 必须 `defer`，避免阻塞 DOM 解析。
- 图片引用相对路径，不要使用绝对 URL（除非是可公开访问的外部素材）。
- `<img>` 必须包含 `alt`；装饰性图片使用 `alt=""`。

### 10.2 CSS 规范

- 变量以 `--` 开头，通用变量放在 `core.css`，项目变量放在主题 CSS。
- 类名采用**小写 + 短横线**：`.my-class-name`（kebab-case）。
- 状态类使用 `active` / `open` / `expanded` / `visible` 等语义化词汇。
- 避免选择器过深（建议 ≤ 3 层），避免 `!important`。
- 新增组件先考虑"是否跨项目通用"，通用 → 放入 `core.css`，否则 → 放入主题 CSS。

### 10.3 JavaScript 规范

- 使用 ES5 语法（`var`、普通 `function`、无解构 / 箭头函数），以兼容 `file://` 协议。
- 所有 `init*` 函数需先检查目标元素是否存在，不存在则静默退出。
- 只在极其必要时向 `window` 挂载全局函数（目前仅 `expandAll` / `collapseAll` / `toggleSection`）。
- `scroll` 事件必须节流（`requestAnimationFrame` 或时间戳节流）。

### 10.4 格式化

- 使用 Prettier 统一格式。运行 `npx prettier --write "**/*.{html,css,js,md,json,yml}"`。
- 使用 2 空格缩进，LF 换行，UTF-8 无 BOM。

---

## 11. 常见问题排查（FAQ）

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| 页面无样式 / 浏览器 404 | CSS / JS 相对路径错误（层级不匹配） | 从 HTML 出发数 `../` 的数量，或检查仓库结构变动 |
| 主题色没有生效 | 主题 CSS `:root` 变量未覆盖 `core.css` | 主题 CSS 必须在 `core.css` **之后** `<link>` |
| 左侧目录不滚动高亮 | `section` 缺少 `id`，或 toc 链接 href 不匹配 | 确保 `href="#xxx"` 与目标 `id="xxx"` 一致 |
| 料理筛选无反应 | `.filter-btn` 缺少 `data-filter` 或 `.dish-card` 缺少 `data-cuisine` | 补齐两个数据属性 |
| GitHub Pages 部署后 404 | ① Pages 尚未激活；② base URL 与子路径冲突；③ 缺少 `.nojekyll` | 在 Settings → Pages 中确认；本项目已包含 `.nojekyll` |
| `file://` 打开某些功能不可用 | 某些浏览器对 file 协议限制跨文件 fetch / import | 使用本地 HTTP 服务器（Python / Node） |
| 图片加载失败 | 图片路径 / 文件名与实际不符；或路径使用了错误的大小写（Linux 服务器区分大小写） | 统一小写路径，提交前本地预览确认 |

---

## 12. 文件索引表（快速跳转）

| 路径 | 角色 | 行数级 |
| --- | --- | --- |
| `index.html` | 首页 / 入口 | 轻量 |
| `styles/core.css` | 全站骨架样式 | 主样式 |
| `styles/themes/home.css` | 首页主题 | 轻量 |
| `styles/themes/dr-stone-science.css` | 石纪元主题 | 中量 |
| `styles/themes/maoyuu-political-economy.css` | 魔王勇者主题 | 中量 |
| `styles/themes/tondemo-skill-food.css` | 流浪美食家主题 | 中量 |
| `styles/themes/shokugeki-no-soma.css` | 食戟之灵主题 | 中量 |
| `scripts/navigation.js` | 全站交互脚本 | 主脚本（~470 行） |
| `content/dr-stone-science/*.html` | 《石纪元》内容页 | 共 10 页 |
| `content/maoyuu-political-economy/*.html` | 《魔王勇者》内容页 | 共 9 页 |
| `content/tondemo-skill-food/*.html` | 流浪美食家内容页 | 共 3 页 |
| `content/shokugeki-no-soma/*.html` | 《食戟之灵》内容页 | 共 11 页 |
| `.github/workflows/deploy.yml` | Pages 自动部署 | 轻量 |
| `.prettierrc` | 格式化配置 | 轻量 |
| `.editorconfig` | 编辑器配置 | 轻量 |
| `jsconfig.json` | VS Code JS 配置 | 轻量 |
| `.nojekyll` | 跳过 Jekyll（GitHub Pages 专用） | 空文件 |
| `LICENSE` | MIT 协议 | — |
| `README.md` | 面向用户与贡献者的项目说明 | 主文档 |
| `docs/code-wiki.md` | 本文件（工程向 Code Wiki） | 主文档 |

---

## 13. 版本与更新记录

- **2026-06-14** — 完成内容模块化重构：石纪元 / 魔王勇者 / 流浪美食家 均从单一大文件拆分为多章节页面；首次引入本 Code Wiki 与标准化的主题 / 脚本规范。

---

## 14. 下一步演进方向（可选）

1. 将所有图片迁移至 WebP 格式以降低体积，并用 Git LFS 托管大文件。
2. 为每个子项目引入独立的内容清单 JSON，由 `navigation.js` 统一渲染目录，减少 HTML 中的手工维护。
3. 引入简单的站内搜索（例如基于预构建 JSON 索引 + `fuse.js` 的轻量方案）。
4. 引入 E2E 测试（Playwright），在 CI 中校验 4 个项目页的样式与目录高亮表现。
5. 引入 PWA 支持，允许离线浏览。
