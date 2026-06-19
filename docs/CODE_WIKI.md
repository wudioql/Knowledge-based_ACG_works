# ACG 知识手册库 — 项目结构规范

> 本文档面向开发者、内容贡献者和项目维护者。如果你只是想浏览内容，请直接访问 [项目主页](https://wudioql.github.io/Knowledge-based_ACG_works/) 或阅读 [README.md](../README.md)。

---

## 项目架构

### 设计哲学

本项目选择**原生技术栈**（HTML5 + CSS3 + Vanilla JavaScript），基于以下考量：

- **零依赖**：无需 npm、构建工具或框架升级，项目可独立运行十年以上
- **零构建**：保存即生效，贡献者无需学习构建流程
- **透明可控**：每一行代码都直接作用于页面，无抽象层带来的调试成本
- **GitHub Pages 原生友好**：静态文件直接托管，无需额外配置

### 目录结构

```
acg-knowledge-handbook/
├── index.html                      # 项目主页（落地页）
├── .nojekyll                       # 禁用 Jekyll 处理（GitHub Pages 配置）
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions 自动部署工作流
├── _shared/                         # 项目级共享资源
│   ├── style.css                   # 主页样式表
│   ├── home-button.css             # 主页按钮样式
│   └── home-button.js              # 主页按钮注入脚本
└── doc/                             # 作品内容目录
    ├── maoyuu/                      # 魔王勇者（政治经济学手册）
    │   ├── index.html               # 作品首页
    │   ├── glossary.html            # 术语表
    │   ├── references.html          # 参考文献
    │   ├── vol-01-*.html            # 各卷内容页（8 卷 + 番外）
    │   └── _shared/                 # 作品级共享资源
    │       ├── style.css            # 作品样式表
    │       └── script.js            # 作品交互脚本
    └── shokugeki_no_soma/           # 食戟之灵（料理全鉴）
        ├── index.html               # 作品首页
        ├── arc-*.html               # 各篇章内容页（10 个篇章）
        └── _shared/                 # 作品级共享资源
            ├── style.css            # 作品样式表
            └── script.js            # 作品交互脚本
```

### 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 页面结构 | HTML5 | 语义化标签，无框架 |
| 样式 | CSS3 | CSS 变量 + 原生选择器，无预处理器 |
| 交互 | Vanilla JavaScript | 模块化函数，无框架 |
| 字体 | Google Fonts (Lora, WorkSans) | 通过 `@import` 引入 |
| 部署 | GitHub Actions + GitHub Pages | 推送即部署 |
| 构建工具 | 无 | 纯静态，零构建 |

---

## 模块体系

### 核心模块

#### `index.html` — 项目主页

- 展示所有作品手册入口卡片
- 显示项目统计数据（作品数、知识点数、学科领域数）
- 包含 Hero 区域和 About 区域

#### `_shared/style.css` — 项目级样式

- 定义全局 CSS 变量（颜色、字体、间距）
- 包含 Header、Hero、Works Card、Footer 样式
- 定义学科标签颜色类（经济、政治、历史等）

#### `_shared/home-button.css` / `home-button.js` — 主页按钮

- 固定定位的圆形返回主页按钮，悬停显示「主页」标签
- **由 CI/CD 在部署时自动注入到所有 `doc/` 下的 HTML 文件**
- 根据 URL 深度动态计算返回主页的相对路径

### 作品模块（通用模板）

每个作品模块遵循以下统一结构：

```
doc/<work-id>/
├── index.html               # 作品入口页：导航、分类索引
├── content-*.html           # 内容页：知识点/料理详情
├── glossary.html            # 术语表（可选）
├── references.html          # 参考文献（可选）
└── _shared/
    ├── style.css            # 作品专属样式：扩展全局变量
    └── script.js            # 作品交互脚本
```

#### 现有作品实例

| 作品 ID | 目录 | 知识领域 | 内容类型 | 内容页命名 |
|---------|------|----------|----------|------------|
| maoyuu | `doc/maoyuu/` | 政治经济学 | 手册 | `vol-01-*.html` ~ `vol-08-*.html` |
| shokugeki | `doc/shokugeki_no_soma/` | 料理学 | 全鉴 | `arc-01-*.html` ~ `arc-10-*.html` |

#### 作品 `_shared/script.js` 通用功能

每个作品的 `script.js` 通常包含以下功能模块：

| 函数 | 职责 |
|------|------|
| `initNavToggle()` | 移动端 Hamburger 菜单展开/收起 |
| `initCollapsibles()` | 绑定折叠按钮点击事件，切换 `aria-expanded` |
| `initFilter()` | 按学科/料理体系筛选卡片 |
| `initBackToTop()` | 滚动超过 400px 显示返回顶部按钮 |
| `initSideToc()` | 侧边目录滚动监听，更新当前高亮链接 |
| `initSmoothScroll()` | 拦截锚点链接，启用平滑滚动 |

---

## 开发规范

### 文件组织规范

- 作品目录使用**小写英文 + 下划线**，如 `shokugeki_no_soma`
- 内容页文件名使用**前缀 + 描述**，如 `vol-01-agricultural-revolution.html`
- 共享资源必须放在 `_shared/` 子目录中
- 所有 HTML 文件使用语义化标签（`header`、`main`、`section`、`article`、`footer`）

### CSS 命名约定

| 前缀 | 用途 | 示例 |
|------|------|------|
| `.site-` | 全局站点元素 | `.site-header`、`.site-nav`、`.site-footer` |
| `.hero-` | 首屏区域 | `.hero-title`、`.hero-lead` |
| `.works-` | 作品卡片区域 | `.works-grid`、`.works-card` |
| `.vol-` | 魔王勇者卷卡 | `.vol-card`、`.vol-title` |
| `.arc-` | 食戟之灵篇章卡 | `.arc-card`、`.arc-title` |
| `.topic-` | 知识点卡片 | `.topic-card`、`.topic-meta` |
| `.dish-` | 料理卡片 | `.dish-card`、`.dish-recipe` |
| `.filter-` | 筛选器控件 | `.filter-group`、`.filter-btn` |
| `.collapsible-` | 可折叠内容 | `.collapsible-header`、`.collapsible-body` |
| `.side-toc` | 侧边目录 | `.side-toc-list`、`.side-toc-link` |
| `.back-to-top` | 返回顶部 | `.back-to-top` |
| `.disc-tag-` | 学科标签 | `.disc-tag-econ`、`.disc-tag-politics` |

### CSS 变量系统

全局变量定义在 `_shared/style.css` 中，作品样式通过覆盖或扩展实现差异化：

```css
/* 全局颜色 */
--bg: #FAFAF5;              /* 背景色 */
--bg2: #F0EDE5;             /* 次要背景 */
--ink: #1A1A2E;             /* 主文字色 */
--muted: #6B7280;           /* 次要文字 */
--rule: #D4CFC5;            /* 分隔线 */
--accent: #8B0000;          /* 主强调色 */
--accent2: #B8860B;         /* 次强调色 */

/* 学科颜色 */
--disc-econ: #1565C0;       /* 经济学 */
--disc-politics: #C62828;   /* 政治学 */
--disc-history: #2E7D32;    /* 历史学 */
--disc-tech: #00838F;       /* 技术 */
--disc-philosophy: #6A1B9A; /* 哲学 */

/* 字体 */
--font-heading: 'Lora', serif;
--font-body: 'WorkSans', sans-serif;
```

新增作品时，如需新学科标签，应在全局 CSS 变量中注册颜色，并在 `.disc-tag-*` 类中使用。

### JavaScript 模块规范

- 每个作品 `script.js` 使用立即执行函数（IIFE）封装，避免全局污染
- 功能按 `initXxx()` 函数拆分，在 DOMContentLoaded 时统一调用
- 优先使用原生 DOM API，避免引入外部库
- 事件委托优先于逐个元素绑定

---

## 扩展指南

### 添加新作品的完整流程

#### 步骤 1：规划内容

确定以下要素：

- **知识领域**：作品涉及的真实知识领域（如军事学、物理学、法学）
- **内容类型**：选择手册、全鉴、年表、地图中的一种（参见 README 内容体系章节）
- **三方对照点**：列出作品中可与学术理论/真实历史对照的关键内容

#### 步骤 2：创建目录

在 `doc/` 下创建新作品文件夹：

```bash
mkdir doc/<work-id>
mkdir doc/<work-id>/_shared
```

创建基础文件：

```bash
touch doc/<work-id>/index.html
touch doc/<work-id>/_shared/style.css
touch doc/<work-id>/_shared/script.js
```

#### 步骤 3：开发页面

1. **复制基础模板**：从现有作品（如 `doc/maoyuu/`）复制 `index.html` 作为起点
2. **修改共享资源路径**：确保 `<link>` 和 `<script>` 的 `href`/`src` 指向 `doc/<work-id>/_shared/`
3. **编写内容页**：按内容类型创建内容 HTML 文件
4. **自定义样式**：在 `_shared/style.css` 中扩展全局变量，添加作品专属样式
5. **添加交互**：在 `_shared/script.js` 中实现筛选、目录、折叠等功能

> **注意**：`home-button.css` 和 `home-button.js` 由 CI/CD 自动注入，无需手动添加。

#### 步骤 4：注册作品

在根目录 `index.html` 的「作品知识手册」区域添加作品卡片：

```html
<a href="doc/<work-id>/" class="works-card">
  <h3>作品名称</h3>
  <p>知识领域 · 内容类型</p>
</a>
```

#### 步骤 5：更新文档

1. 在 [README.md](../README.md) 的作品总览表格中添加新行
2. 在本文档的「现有作品实例」表格中添加新行
3. 如新增学科标签，更新本文档的 CSS 变量说明

### 主页集成检查清单

- [ ] 作品目录创建在 `doc/<work-id>/`
- [ ] `_shared/style.css` 和 `_shared/script.js` 已创建
- [ ] 至少一个内容页已编写
- [ ] `index.html` 的共享资源路径正确
- [ ] 根目录 `index.html` 已添加作品卡片
- [ ] README.md 作品表格已更新
- [ ] CODE_WIKI.md 作品实例表格已更新
- [ ] 本地预览确认页面渲染正常
- [ ] 移动端导航和筛选功能测试通过

---

## 部署架构

### GitHub Actions 工作流

`.github/workflows/deploy.yml` 负责自动部署：

```
触发条件:
  - push 到 main/master 分支
  - 手动 workflow_dispatch

步骤:
  1. Checkout code
  2. 遍历 doc/ 下所有 .html 文件
     - 计算相对路径深度
     - 注入 home-button.css 链接到 </head>
     - 注入 home-button.js 脚本到 </body>
  3. Upload artifact
  4. Deploy to GitHub Pages
```

### 主页按钮注入逻辑

部署时，工作流自动为每个 `doc/` 下的 HTML 文件注入返回主页的按钮：

- 解析文件路径，计算相对于项目根的深度
- 生成对应的 `../` 前缀
- 在 `</head>` 前注入 `<link rel="stylesheet" href="{prefix}_shared/home-button.css">`
- 在 `</body>` 前注入 `<script src="{prefix}_shared/home-button.js"></script>`

---

## 设计模式

### HTML 页面结构模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题 | 作品名称 | ACG 知识手册库</title>
  <link rel="stylesheet" href="_shared/style.css">
  <!-- home-button.css 由 CI/CD 自动注入 -->
</head>
<body>
  <header class="site-header">...</header>

  <section class="hero">
    <h1>页面标题</h1>
    <p class="hero-lead">页面描述</p>
  </section>

  <main class="container">
    <!-- 内容区域 -->
  </main>

  <footer class="site-footer">...</footer>
  <button class="back-to-top" aria-label="返回顶部">↑</button>

  <script src="_shared/script.js"></script>
  <!-- home-button.js 由 CI/CD 自动注入 -->
</body>
</html>
```

### 依赖关系

```
index.html
├── _shared/style.css
└── (无 JS)

doc/<work-id>/*.html
├── doc/<work-id>/_shared/style.css
├── _shared/home-button.css    ← CI/CD 注入
└── _shared/home-button.js     ← CI/CD 注入
    └── doc/<work-id>/_shared/script.js
```

---

## 内容数据

### 魔王勇者 — 知识体系

| 学科 | 知识点数 | 代表概念 |
|------|----------|----------|
| 经济学 | 12 | 比较优势、重商主义、通货膨胀 |
| 政治学 | 12 | 社会契约论、三权分立、博弈论 |
| 历史学 | 12 | 农业革命、宗教改革、金融革命 |
| 技术制度 | 5 | 技术创新、专利制度、教育制度 |
| 思想哲学 | 5 | 启蒙运动、女性主义、骑士精神 |

**核心学者**：亚当·斯密、大卫·李嘉图、凯恩斯、熊彼特、洛克、卢梭、孟德斯鸠等

### 食戟之灵 — 料理体系

| 篇章 | 话数范围 | 料理数 |
|------|----------|--------|
| 入学篇 | 1-13 话 | ~12 |
| 住宿研修 | 14-27 话 | ~20 |
| 秋季选拔 | 28-60 话 | ~23 |
| 食戟 vs 久我 | 61-87 话 | ~16 |
| 实习篇 | 88-106 话 | ~11 |
| 月飨祭 | 107-137 话 | ~17 |
| 远月列车 | 138-158 话 | ~10 |
| 联队食戟 | 159-217 话 | ~29 |
| THE BLUE | 218-315 话 | ~55 |
| 番外篇 | 3 话 | ~5 |

**料理体系**：日式、法式、意式、中式、东南亚、分子美食学等
