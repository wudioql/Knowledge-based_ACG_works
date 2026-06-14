# ACG 知识库 | Knowledge-based ACG Works

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-brightgreen.svg)](https://pages.github.com/)

基于动画、漫画、游戏作品的知识整理与科普项目,涵盖科学知识、政治经济学、料理文化等多个领域。

## 📚 项目内容

| 项目 | 目录 | 内容 | 状态 |
|------|------|------|------|
| 《石纪元》科学知识手册 | `content/dr-stone-science/` | 从石器到火箭的人类科技发展史 | ✅ 已完结 |
| 《魔王勇者》政治经济学手册 | `content/maoyuu-political-economy/` | 小说中的政治经济学概念深度解析 | ✅ 已完结 |
| 异世界流浪美食家料理图鉴 | `content/tondemo-skill-food/` | 两季动画料理大全与图文对照 | 🔄 持续更新 |
| 《食戟之灵》料理内容文档 | `content/shokugeki-no-soma/` | 全篇料理对决与剧情梳理(10篇章) | ✅ 已完结 |

## 🌐 在线访问

> 项目尚未部署至 GitHub Pages，部署完成后将在此更新访问链接。

## 🚀 本地预览

```bash
# 方法1: 使用Python内置服务器
python -m http.server 8000

# 方法2: 使用Node.js的serve
npx serve .

# 方法3: 直接在浏览器中打开index.html
```

然后访问 `http://localhost:8000` 或直接打开 `index.html`。

## 🛠️ 技术栈

- **前端**: 纯静态 HTML / CSS / JavaScript（零构建、零依赖）
- **样式架构**: `styles/core.css`（全站骨架） + `styles/themes/*.css`（各项目主题）
- **脚本架构**: `scripts/navigation.js`（全站通用的导航 / 折叠 / 目录 / 筛选 / 平滑滚动）
- **托管**: GitHub Pages
- **部署**: GitHub Actions 自动部署
- **字体**: Google Fonts CDN（Lora / Work Sans / Noto Serif SC）+ 本地 `ArsenalSC-Regular.ttf`
- **图表**: ECharts CDN
- **流程图**: Mermaid CDN

## 🏗️ 架构说明（重构后）

本项目采用 **内容层 / 骨架层 / 主题层** 三层分离的静态页面架构，避免在各 HTML 中重复写入样式与脚本：

```
index.html ──┐
content/*/index.html  ─┤  内容层（只写语义 HTML，不写任何 <style> 或 <script>）
content/*/arc-*.html  ─┘

styles/core.css  ──────── 骨架层（reset / container / hero / section-title /
                          card / tag / filter-bar / back-to-top / side-toc /
                          site-header / site-nav / nav-toggle / site-footer /
                          响应式断点 / 打印样式）

styles/themes/home.css           ┐
styles/themes/dr-stone-science.css      │
styles/themes/maoyuu-political-economy.css │  主题层（只写 CSS 变量
styles/themes/tondemo-skill-food.css   │   与"只在该项目出现的组件"样式）
styles/themes/shokugeki-no-soma.css    ┘

scripts/navigation.js  ─── 脚本层（统一的导航切换 / 折叠 / 目录高亮 / 筛选 / 平滑滚动 / back-to-top）
```

**为什么这样分？**
- 样式/脚本不再写死在每个 HTML 里，改动只需要改一个地方，全站立即生效
- 新增作品只需「新建一个 `content/<name>/index.html` + 新建一个 `styles/themes/<name>.css`」，复制下面的模板即可
- 每个项目保持自己的品牌色彩与视觉气质（石纪元暗色科技 / 魔王勇者酒红学术 / 流浪美食家暖色料理 / 食戟之灵白纸料理）

### 主题变量规范（最小集合）

每个主题 CSS 必须至少定义以下变量（覆盖 `core.css` 中的默认值）：

```css
:root {
  --bg:             /* 页面主体背景 */
  --bg2:            /* 次要背景（卡片、表格头、侧边栏） */
  --ink:            /* 正文文字颜色 */
  --muted:          /* 次要文字 / 辅助说明 */
  --rule:           /* 边框 / 分割线 */
  --accent:         /* 主题色（链接、按钮、强调） */
  --accent2:        /* 第二强调色（常用于徽章、次要强调） */
  --ink-on-accent:  /* 放在 accent 背景上的文字颜色（通常是白） */

  --font-heading:   /* 标题字体 */
  --font-body:      /* 正文字体 */
  --content-width:  /* 正文最大宽度（如 1080px） */
}
```

## 📋 项目结构

```
Knowledge-based ACG works/
├── .github/                    # GitHub 配置
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 部署配置
├── assets/                     # 静态资源
│   ├── fonts/                 # 字体文件
│   │   └── ArsenalSC-Regular.ttf
│   └── images/                # 图片资源
│       ├── dr-stone-science/
│       ├── maoyuu-political-economy/
│       ├── shokugeki-no-soma/
│       └── tondemo-skill-food/
├── content/                    # 内容页面（仅写语义 HTML，不配样式）
│   ├── dr-stone-science/      # 《石纪元》项目
│   │   └── index.html
│   ├── maoyuu-political-economy/  # 《魔王勇者》项目
│   │   └── index.html
│   ├── shokugeki-no-soma/     # 《食戟之灵》项目
│   │   ├── index.html
│   │   └── arc-*.html         # 10 个篇章页
│   └── tondemo-skill-food/    # 异世界流浪美食家项目
│       └── index.html
├── scripts/                    # 共享 JavaScript 脚本
│   └── navigation.js           # 全站通用交互（nav / collapsible / side-toc / filter / smooth-scroll）
├── styles/                     # 样式文件（骨架 + 主题）
│   ├── core.css                # 全站共享骨架（reset / 布局 / 通用组件 / 响应式 / 打印）
│   └── themes/                 # 各项目主题（CSS 变量 + 项目专属组件样式）
│       ├── home.css            # 首页主题
│       ├── dr-stone-science.css
│       ├── maoyuu-political-economy.css
│       ├── tondemo-skill-food.css
│       └── shokugeki-no-soma.css
├── index.html                  # 主入口页面
├── .editorconfig              # 编辑器配置
├── .prettierrc               # 代码格式化配置
├── jsconfig.json              # JavaScript 项目配置
├── .gitignore
├── .nojekyll
├── LICENSE
└── README.md
```

### 目录说明

| 目录 | 说明 |
|------|------|
| `assets/` | 静态资源文件（字体、图片等） |
| `content/` | 各作品的内容页面（**只写语义 HTML**，不配 `<style>` / `<script>`） |
| `scripts/` | 共享 JavaScript 脚本（统一交互） |
| `styles/core.css` | 全站骨架样式（**所有项目共用**） |
| `styles/themes/*.css` | 各项目主题（颜色变量 + 项目专属组件样式） |

## 🔧 部署说明

### GitHub Pages部署流程

1. **初始化Git仓库**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ACG知识库项目"
   ```

2. **创建GitHub仓库**:
   - 在GitHub上创建新仓库
   - 不要初始化README、LICENSE或.gitignore(已在本地创建)

3. **推送代码**:
   ```bash
   git remote add origin https://github.com/<你的用户名>/<仓库名>.git
   git branch -M main
   git push -u origin main
   ```

4. **启用GitHub Pages**:
   - 进入仓库 Settings > Pages
   - Source选择"GitHub Actions"
   - 自动触发部署

5. **访问网站**:
   - 部署完成后访问 `https://<你的用户名>.github.io/<仓库名>/`

### 自动部署配置

项目已配置GitHub Actions自动部署:
- 推送到`main`或`master`分支自动触发部署
- 部署配置文件: `.github/workflows/deploy.yml`

## 🔄 更新与维护

### 添加新作品（完整流程 + 可直接复制的模板）

1. 在 `content/` 下创建新的子项目目录（例如 `content/my-new-work/`），创建 `index.html`，内容从下面"模板 A"复制后填充章节
2. 在 `styles/themes/` 下创建新的主题文件（例如 `my-new-work.css`），内容从下面"模板 B"复制后调整颜色
3. 在 `assets/images/my-new-work/` 下放置图片资源（如需要）
4. 在 **首页 `index.html`** 的 `.projects-grid` 中追加一张新卡片（复制现有 `<a class="project-card">` 改一下文字和链接）
5. 更新 README 的"项目内容"表格与"致谢"段落
6. `python -m http.server 8000` 本地预览确认后提交

### 模板 A — 新作品 HTML（复制粘贴即可）

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

  <!-- 统一顶部导航（logo + 4 个作品入口） -->
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

  <!-- 可选：移动端目录按钮（如无左侧 sidebar 可不加） -->
  <button class="sidebar-toggle" data-sidebar-toggle aria-label="展开目录">☰ 目录</button>

  <!-- 可选：左侧/右侧目录（如需要） -->
  <nav class="sidebar-toc">
    <h4>目录</h4>
    <ol>
      <li><a href="#ch1">第一章 · 概述</a></li>
      <li><a href="#ch2">第二章 · 核心概念</a></li>
    </ol>
  </nav>

  <!-- 正文（核心内容从这里开始写，你只要专注内容就行） -->
  <main class="main-content">
    <section class="hero">
      <div class="container">
        <h1>XXX</h1>
        <p class="subtitle">一句话介绍这个作品</p>
      </div>
    </section>

    <section class="container">
      <h2 class="section-title">第一章 <span class="title-en">Chapter 1</span></h2>
      <p>你的正文内容……</p>
    </section>

    <!-- 更多章节…… -->
  </main>

  <!-- 统一页脚 -->
  <footer class="site-footer">
    <div class="container">
      <p>XXX · ACG 知识库</p>
      <p class="copyright">原作：XXX。本站内容采用 MIT 协议开源，图片素材版权归原作者所有。</p>
    </div>
  </footer>

</body>
</html>
```

### 模板 B — 新作品主题 CSS（复制粘贴即可）

```css
/* ============================================
   XXX — 主题样式
   ============================================ */

:root {
  /* 颜色（改这几行就能换整个项目的"气质"） */
  --bg:         #ffffff;  /* 页面主背景 */
  --bg2:        #f5f5f5;  /* 次要背景（卡片、表格头） */
  --ink:        #1a1a1a;  /* 正文文字 */
  --muted:      #777777;  /* 次要文字 */
  --rule:       #e5e5e5;  /* 边框 / 分割线 */
  --accent:     #c0392b;  /* 主题色 */
  --accent2:    #f39c12;  /* 第二强调色 */
  --ink-on-accent: #ffffff;

  /* 字体与尺寸 */
  --font-heading: 'Lora', 'Noto Serif SC', Georgia, serif;
  --font-body:    'Work Sans', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --content-width: 1080px;
}

/* ===== 项目专属组件（只有这个项目会用到，写在这里）===== */

/* 例如：
.my-special-card {
  background: var(--bg2);
  border-radius: 10px;
  padding: 1.5rem;
  border-left: 4px solid var(--accent);
}

.my-badge {
  display: inline-block;
  padding: 0.2em 0.6em;
  border-radius: 4px;
  background: rgba(255,193,7,.15);
  color: var(--accent);
}
*/

/* ===== 响应式微调（如需要，可在主题层再做细调） ===== */
@media (max-width: 768px) {
  /* 项目专属的响应式覆盖 */
}

@media print {
  /* 项目专属的打印样式覆盖 */
}
```

**使用原则**：
- 通用组件（card / tag / hero / site-header / container / filter-bar / back-to-top 等）都在 `core.css` 中已经定义好了，主题 CSS 只管"颜色变量 + 只在这个项目出现的特殊组件"
- 切勿在任何 `content/*.html` 中再写 `<style>` 或内联脚本，保持内容层只写内容

### 更新现有作品

1. 修改对应子项目的HTML文件（或其主题 CSS）
2. 更新图片资源（如需）
3. 推送更改到GitHub，自动部署

### 内容更新流程

```bash
# 1. 修改内容文件
# 2. 本地测试
python -m http.server 8000

# 3. 提交更改
git add .
git commit -m "Update: 更新XXX作品内容"

# 4. 推送到GitHub
git push origin main
```

## 📝 贡献指南

欢迎贡献新的ACG作品知识内容!

### 贡献流程

1. Fork本仓库
2. 创建新的分支 (`git checkout -b feature/new-work`)
3. 按上面"添加新作品"的流程，新增 `content/<name>/index.html` + `styles/themes/<name>.css`
4. **不要**在 HTML 中写 `<style>` 或内联 `<script>`——样式交给 `core.css` 与 `themes/*.css`，交互交给 `scripts/navigation.js`
5. 提交更改 (`git commit -m "Add: 新作品XXX"`)
6. 推送到分支 (`git push origin feature/new-work`)
7. 创建Pull Request

### 内容规范

- 使用UTF-8编码的HTML文件
- 图片使用WebP或JPEG格式,尽量压缩
- 内容准确,注明参考来源
- 遵守相关版权规定

## ⚖️ 版权声明

- 本项目采用MIT许可证开源
- 项目内容为粉丝整理的非官方资料
- 图片素材版权归原作者所有
- 仅供学习参考,请勿用于商业用途

## 📚 参考来源

各子项目页面底部列有详细参考来源,包括:
- 官方网站
- Fandom Wiki
- 学术文献
- 新闻报道

## 🙏 致谢

感谢所有原作品作者和创作者:
- 《石纪元》: 稻垣理一郎 × Boichi
- 《魔王勇者》: 橙乃真希
- 《食戟之灵》: 附田祐斗 × 佐伯俊
- 《异世界流浪美食家》: 远野

---

**最后更新**: 2026-06-14（完成全站骨架重构：core.css + themes/*.css + navigation.js 统一架构）
