# ACG 知识库 · Knowledge-based ACG Works

> 基于动画、漫画、游戏作品的知识整理与科普项目。  
> 零构建、零依赖的纯静态站点，托管于 GitHub Pages。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-brightgreen.svg)](https://pages.github.com/)
[![Built with ❤ — Vanilla HTML/CSS/JS](https://img.shields.io/badge/Built%20with-vanilla%20HTML%2FCSS%2FJS-f39c12.svg)](#)

---

## 这是什么？

**ACG 知识库**是一个以 ACG（动画 · 漫画 · 游戏）作品为索引，对其中**非虚构知识**（科学原理、政治经济学、料理文化等）进行系统整理与科普的**静态内容站**。

- 📖 **《石纪元》科学知识手册** — 从石器到火箭的人类科技发展史。
- 🏛️ **《魔王勇者》政治经济学手册** — 小说中政治经济学概念的深度解析。
- 🍜 **异世界流浪美食家料理图鉴** — 两季动画中出现的料理图文对照。
- 🔥 **《食戟之灵》料理内容文档** — 全篇 10 篇章的料理对决与剧情梳理。

本站点**不**包含任何动画 / 漫画原作的版权内容，仅以粉丝身份整理知识性材料。

---

## 快速开始

本项目是零构建项目，源码即产物，三种方式任选其一即可在本地查看：

```bash
# 方式 A — Python 内置 HTTP 服务器（推荐本地开发）
python3 -m http.server 8000

# 方式 B — Node.js serve
npx serve .

# 方式 C — 直接双击 index.html（最简单，也能运行）
```

随后在浏览器中访问 <http://localhost:8000>（或直接 `index.html`）。

> 在线访问（如已部署）：<https://<username>.github.io/<repo>/>

---

## 项目内容总览

| 子项目 | 目录 | 页面数 | 主题色 | 状态 |
| --- | --- | --- | --- | --- |
| 《石纪元》科学知识手册 | `content/dr-stone-science/` | 10（封面 + 8 章 + 附录） | 深蓝绿 `#00b4d8` | ✅ 已完结 |
| 《魔王勇者》政治经济学手册 | `content/maoyuu-political-economy/` | 9（概览 + 5 卷 + 外传 + 分析） | 酒红 `#b33a3a` | ✅ 已完结 |
| 异世界流浪美食家料理图鉴 | `content/tondemo-skill-food/` | 3（封面 + 两季） | 暖色 `#e07a5f` | 🔄 持续更新 |
| 《食戟之灵》料理内容文档 | `content/shokugeki-no-soma/` | 11（封面 + 10 篇章） | 白纸红 `#c0392b` | ✅ 已完结 |

---

## 技术架构（一句话）

**内容层 · 骨架层 · 主题层 · 脚本层 —— 四层分离，零构建部署。**

```
index.html / content/*/*.html   ← 内容层（只写语义 HTML）
          │
     ┌────┼────┐
     ▼    ▼    ▼
  styles/  styles/       scripts/
  core.css themes/*.css  navigation.js
   (骨架)   (主题)          (交互)
```

- **骨架层 `styles/core.css`** — Reset / Typography / Container / Hero / Card / Tag / Filter / Sidebar / TOC / Site Header / Footer / Back-to-top / 响应式断点 / 打印样式。
- **主题层 `styles/themes/*.css`** — 每个子项目通过覆盖 `:root` 的 CSS 变量完成换肤，并定义自己的项目专属组件（料理卡片 `dish-card` / 章节栅格 `arc-grid` / 树形目录 `toc-tree` 等）。
- **脚本层 `scripts/navigation.js`** — 全站唯一的 JS 文件，IIFE 封装的 ES5 代码，提供导航切换、折叠展开、滚动高亮、平滑滚动、料理筛选、自动生成目录树等交互增强。
- **内容层 `content/*/*.html`** — 只写语义化 HTML，不写 `<style>` 或内联脚本。新增作品即新增目录 + HTML + 主题 CSS。

详细工程向文档见 [`docs/code-wiki.md`](docs/code-wiki.md)。

---

## 目录结构

```
.
├── index.html                  # 站点首页（4 张项目入口卡片）
├── README.md                   # 本文件（用户 + 贡献者指南）
│
├── assets/                     # 静态资源
│   ├── fonts/ArsenalSC-Regular.ttf
│   └── images/<子项目目录>/...
│
├── content/                    # 内容页（语义 HTML 为主）
│   ├── dr-stone-science/
│   ├── maoyuu-political-economy/
│   ├── shokugeki-no-soma/
│   └── tondemo-skill-food/
│
├── scripts/
│   └── navigation.js           # 全站唯一 JS（IIFE + ES5）
│
├── styles/
│   ├── core.css                # 全站骨架样式
│   └── themes/
│       ├── home.css            # 首页主题（深色）
│       ├── dr-stone-science.css
│       ├── maoyuu-political-economy.css
│       ├── shokugeki-no-soma.css
│       └── tondemo-skill-food.css
│
├── .github/workflows/deploy.yml   # GitHub Actions Pages 部署
├── .editorconfig               # 跨编辑器格式约定
├── .prettierrc                # Prettier 格式化配置
├── jsconfig.json              # VS Code 下的 JS 配置
├── .nojekyll                  # 跳过 GitHub Pages 的 Jekyll 处理
├── .gitignore
├── LICENSE                    # MIT
└── docs/
    └── code-wiki.md           # 工程向 Code Wiki（开发与贡献者必读）
```

---

## 新增作品页（6 步即可）

> 新贡献者不需要了解任何构建工具，只需会写基本 HTML 即可。

### 1 新建目录与首页

```
content/my-new-work/
├── index.html   ← 封面 + 目录
└── chapter-01.html ... （按需拆分章节页）
```

### 2 新建主题

```
styles/themes/my-new-work.css
```

至少覆盖以下 CSS 变量（其余默认继承自 `core.css`）：

```css
:root {
  --bg:             /* 页面背景 */
  --bg2:            /* 次要背景 / 卡片背景 */
  --ink:            /* 正文文字颜色 */
  --muted:          /* 次要文字 */
  --rule:           /* 边框 / 分割线 */
  --accent:         /* 主题色 */
  --accent2:        /* 第二强调色 */
  --ink-on-accent:  /* 放在 accent 背景上的文字（通常是白） */

  --font-heading:   /* 标题字体 */
  --font-body:      /* 正文字体 */
  --content-width:  /* 正文最大宽度（1080 / 1200 等） */
}
```

### 3 放置图片资源

```
assets/images/my-new-work/...
```

### 4 在 `index.html` 添加入口卡片

在 `.projects-grid` 中追加：

```html
<a href="./content/my-new-work/index.html" class="project-card">
  <div class="project-icon">🆕</div>
  <h2>新作品标题</h2>
  <p>一句话介绍。</p>
  <div class="project-meta">
    <span class="project-tag">分类标签</span>
    <span class="project-arrow">→</span>
  </div>
</a>
```

### 5 校验

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000/
# 确认新页面样式正确、图片加载正常、顶部导航可用
```

### 6 提交并推送

```bash
git add .
git commit -m "feat: add my-new-work"
git push origin main
# GitHub Actions 会自动部署至 Pages
```

---

## 开发与贡献指南

### 代码规范

- **HTML**：语义化结构，UTF-8；**禁止**在 `content/*.html` 内写 `<style>` 或内联脚本。
- **CSS**：变量化换肤，类名使用 kebab-case（`my-class-name`）；通用样式放在 `core.css`，项目专属样式放在 `themes/*.css`。
- **JavaScript**：使用 ES5 语法、IIFE 封装；目标元素不存在即静默退出；`scroll` 事件必须节流。
- **格式化**：EditorConfig（2 空格、LF、UTF-8）+ Prettier：
  ```bash
  npx prettier --write "**/*.{html,css,js,md,json,yml}"
  ```

### 想贡献内容？

1. **新增作品**：按上面"新增作品页"6 步流程操作。
2. **完善现有内容**：直接编辑对应目录的 HTML / CSS 文件。
3. **修复问题**：修 bug 请在 commit 里写清楚问题与解决方案。
4. Fork → 分支 → commit → PR。

### 版权与使用约定

- 项目代码采用 **MIT 协议**开源。
- 图片素材等版权归原作者所有，本站仅作知识科普用途。
- 内容为**粉丝整理的非官方资料**，不代表原作者观点。

---

## 部署

本项目使用 **GitHub Actions → GitHub Pages**：

| 步骤 | 文件 / 操作 |
| --- | --- |
| Workflow 文件 | `.github/workflows/deploy.yml` |
| 触发 | 推送到 `main` / `master`，或在 GitHub 手动 `workflow_dispatch` |
| 权限 | `contents: read` · `pages: write` · `id-token: write` |
| 一次性操作 | 仓库 Settings → Pages → Source 选择 **GitHub Actions** |

推送后，工作流会依次执行：

```
actions/checkout@v5           拉取仓库
actions/configure-pages@v6    配置 Pages 环境（OIDC token / base URL）
actions/upload-pages-artifact@v5   将整个仓库打包为 artifact（path: '.'）
actions/deploy-pages@v5       部署至 GitHub Pages
```

---

## 更多文档

详细工程向文档（目录职责、关键类与函数说明、依赖关系、常见问题排查等），请见 [`docs/code-wiki.md`](docs/code-wiki.md)。

---

## 致谢

- 《石纪元》（Dr.STONE） · 稲垣理一郎 × Boichi
- 《魔王勇者》 · 橙乃真希
- 《食戟之灵》 · 附田祐斗 × 佐伯俊
- 《拥有超常技能的异世界流浪美食家》 · 远野

---

**最后更新**：2026-06-14（内容模块化重构：石纪元 / 魔王勇者 / 流浪美食家 均由单一大文件拆分为多章节页）
