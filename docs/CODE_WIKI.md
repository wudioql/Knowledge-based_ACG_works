# ACG 知识手册库 — 项目结构规范

## 项目概述

**ACG 知识手册库**（ACG Knowledge Handbook）是一个静态HTML网站项目，通过GitHub Pages托管。网站从动漫与游戏中挖掘真实世界的知识，建立"虚构作品内容 ↔ 学术理论 ↔ 真实历史"的三方对照体系。

## 项目架构

### 目录结构

```
acg-knowledge-handbook/
├── index.html                      # 项目主页（落地页）
├── .nojekyll                       # 禁用 Jekyll 处理（GitHub Pages 配置）
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions 自动部署工作流
├── _shared/                         # 项目级共享资源（根级别）
│   ├── style.css                   # 主页样式表
│   ├── home-button.css             # 主页按钮样式
│   └── home-button.js             # 主页按钮注入脚本
└── doc/                            # 作品内容目录
    ├── maoyuu/                     # 魔王勇者（政治经济学手册）
    │   ├── index.html               # 作品首页
    │   ├── glossary.html            # 术语表
    │   ├── references.html          # 参考文献
    │   ├── vol-01-*.html            # 各卷内容页（8卷+番外）
    │   └── _shared/                 # 作品级共享资源
    │       ├── style.css           # 作品样式表
    │       └── script.js           # 作品交互脚本
    └── shokugeki_no_soma/          # 食戟之灵（料理全鉴）
        ├── index.html               # 作品首页
        ├── arc-*.html              # 各篇章内容页（10个篇章）
        └── _shared/                 # 作品级共享资源
            ├── style.css           # 作品样式表
            └── script.js           # 作品交互脚本
```

### 技术栈

| 类别 | 技术 |
|------|------|
| 页面结构 | HTML5（原生，无框架） |
| 样式 | CSS3（原生，无预处理器） |
| 交互 | Vanilla JavaScript（原生，无框架） |
| 部署 | GitHub Actions + GitHub Pages |
| 托管 | GitHub Pages（静态托管） |
| 构建工具 | 无（纯静态） |

### 部署架构

```
Push to main/master
       │
       ▼
  GitHub Actions
       │
       ├── Checkout code
       │
       ├── Inject home-button.css/js into all doc/*.html
       │      (自动化注入，路径深度计算)
       │
       └── Deploy to GitHub Pages
                 │
                 ▼
           GitHub Pages
           (your-username.github.io/acg-knowledge-handbook/)
```

## 模块职责

### 1. 主页模块（Project Root）

#### `index.html` — 项目落地页
- 展示所有作品手册入口
- 显示项目统计数据（作品数、知识点数、学科领域数）
- 包含 Hero 区域和 About 区域

#### `_shared/style.css` — 项目级样式
- 定义全局 CSS 变量（颜色、字体、间距）
- 包含 Header、Hero、Works Card、Footer 样式
- 定义 tag 颜色类（经济、政治、历史等）

#### `_shared/home-button.css` — 主页按钮样式
- 固定定位的圆形返回主页按钮
- 悬停显示"主页"标签

#### `_shared/home-button.js` — 主页按钮注入脚本
- 自动检测当前页面是否为项目主页
- 根据 URL 深度计算相对路径
- 动态创建并注入主页按钮元素
- **由 CI/CD 在部署时注入到所有 `doc/` 下的 HTML 文件**

### 2. 魔王勇者模块（`doc/maoyuu/`）

#### 内容结构
- **索引页**：`index.html` — 卷导航、理论分类、学者著作索引
- **内容页**：`vol-01-agricultural-revolution.html` 等 — 各卷知识点详情
- **辅助页**：`glossary.html`（术语表）、`references.html`（参考文献）

#### `_shared/style.css` — 作品样式
- 扩展全局样式变量
- 定义 Volume Card、Theory Card、Scholar Card 样式
- 定义 Comparison Table（三方对照表）样式
- 定义 Side TOC、Collapsible、Back to Top 样式

#### `_shared/script.js` — 作品交互脚本
```javascript
// 主要功能
initNavToggle()      // 移动端导航切换
initCollapsibles()   // 可折叠内容区
initFilter()         // 知识点筛选（按学科）
initBackToTop()      // 返回顶部按钮
initSideToc()         // 侧边目录导航（滚动高亮）
initSmoothScroll()   // 平滑滚动
```

### 3. 食戟之灵模块（`doc/shokugeki_no_soma/`）

#### 内容结构
- **索引页**：`index.html` — 篇章导航、料理体系分类、烹饪技法索引
- **内容页**：`arc-01-enrollment.html` 等 — 各篇章料理详情

#### `_shared/style.css` — 作品样式
- 定义 Arc Card、Stats、Cuisine Card 样式
- 定义 Dish Card（料理卡片）样式
- 定义 Recipe Section（食谱步骤）样式
- 定义 Battle Section（食戟对决）样式

#### `_shared/script.js` — 作品交互脚本
```javascript
// 主要功能
initNavToggle()      // 移动端导航切换
initCollapsibles()   // 可折叠内容区
initFilter()         // 料理筛选（按料理体系）
initBackToTop()      // 返回顶部按钮
initSideToc()         // 侧边目录导航
initSmoothScroll()   // 平滑滚动
```

### 4. CI/CD 模块（`.github/workflows/deploy.yml`）

#### 部署工作流
```yaml
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

## 关键类与函数说明

### JavaScript 函数

#### `home-button.js` — 主页按钮注入

```javascript
// 检测当前是否为项目主页
function isProjectHomepage() {
  // 返回 true 如果路径匹配项目根
}

// 计算返回项目根的相对路径
function getRootPath() {
  // 解析 URL 路径段，计算 ../ 数量
  // 例: /doc/maoyuu/vol-01.html -> ../../../
}
```

#### `script.js`（魔王勇者/食戟之灵共用）

| 函数 | 职责 |
|------|------|
| `initNavToggle()` | 移动端 Hamburger 菜单展开/收起 |
| `initCollapsibles()` | 绑定折叠按钮点击事件，切换 `aria-expanded` |
| `initFilter()` | 按学科/料理体系筛选卡片 |
| `initBackToTop()` | 滚动超过 400px 显示返回顶部按钮 |
| `initSideToc()` | 侧边目录滚动监听，更新当前高亮链接 |
| `initSmoothScroll()` | 拦截锚点链接，启用平滑滚动 |

### CSS 类命名约定

| 前缀 | 用途 |
|------|------|
| `.site-` | 全局站点元素（header, nav, footer） |
| `.hero-` | 首屏区域 |
| `.works-` | 作品卡片区域 |
| `.vol-` | 魔王勇者卷卡 |
| `.arc-` | 食戟之灵篇章卡 |
| `.topic-` | 知识点卡片 |
| `.dish-` | 料理卡片 |
| `.filter-` | 筛选器控件 |
| `.collapsible-` | 可折叠内容 |
| `.side-toc` | 侧边目录 |
| `.back-to-top` | 返回顶部 |
| `.chapter-nav` | 篇章导航 |
| `.disc-tag-` | 学科标签 |
| `.tag-` | 通用标签 |

### CSS 变量

```css
/* 全局颜色 */
--bg: #FAFAF5;           /* 背景色 */
--bg2: #F0EDE5;          /* 次要背景 */
--ink: #1A1A2E;          /* 主文字色 */
--muted: #6B7280;        /* 次要文字 */
--rule: #D4CFC5;         /* 分隔线 */
--accent: #8B0000;       /* 主强调色 */
--accent2: #B8860B;       /* 次强调色 */

/* 学科颜色 */
--disc-econ: #1565C0;    /* 经济学 */
--disc-politics: #C62828; /* 政治学 */
--disc-history: #2E7D32; /* 历史学 */
--disc-tech: #00838F;    /* 技术 */
--disc-philosophy: #6A1B9A; /* 哲学 */

/* 字体 */
--font-heading: 'Lora', serif;
--font-body: 'WorkSans', sans-serif;
```

## 依赖关系

### 外部依赖

| 依赖 | 用途 | 引入方式 |
|------|------|----------|
| Google Fonts (Lora, WorkSans) | 字体 | `@import` in CSS |

### 内部依赖

```
index.html
├── _shared/style.css
└── (无 JS)

doc/maoyuu/*.html
├── doc/maoyuu/_shared/style.css
├── _shared/home-button.css    ← CI/CD 注入
└── _shared/home-button.js    ← CI/CD 注入
    └── doc/maoyuu/_shared/script.js

doc/shokugeki_no_soma/*.html
├── doc/shokugeki_no_soma/_shared/style.css
├── _shared/home-button.css    ← CI/CD 注入
└── _shared/home-button.js    ← CI/CD 注入
    └── doc/shokugeki_no_soma/_shared/script.js
```

## 项目运行方式

### 本地预览

```bash
# 方式一：Python HTTP Server
cd acg-knowledge-handbook
python3 -m http.server 8080
# 访问 http://localhost:8080

# 方式二：Node.js http-server
npx http-server -p 8080

# 方式三：直接用浏览器打开 index.html（部分功能受限）
```

### 部署流程

```bash
# 1. 本地开发测试
# 2. 推送到 GitHub
git add .
git commit -m "Update content"
git push origin main

# 3. GitHub Actions 自动触发部署
#    - 无需手动操作
```

### 添加新作品

1. 在 `doc/` 下创建新作品文件夹（如 `doc/新作品名/`）
2. 创建 `_shared/` 目录，包含 `style.css` 和 `script.js`
3. 创建作品内容 HTML 文件
4. 在项目根 `index.html` 添加作品卡片入口
5. 推送后 CI/CD 自动注入主页按钮

## 设计模式

### HTML 页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <link rel="stylesheet" href="作品_shared/style.css">
  <link rel="stylesheet" href="项目级_shared/home-button.css"> <!-- CI/CD 注入 -->
</head>
<body>
  <header class="site-header">...</header>
  <section class="hero">...</section>
  <main class="container">
    <!-- 内容区域 -->
  </main>
  <footer class="site-footer">...</footer>
  <button class="back-to-top">↑</button>
  <script src="作品_shared/script.js"></script>
  <script src="项目级_shared/home-button.js"></script> <!-- CI/CD 注入 -->
</body>
</html>
```

### CI/CD 注入逻辑

```bash
# 遍历所有 doc/*.html 文件
for f in doc/*/*.html; do
  # 计算相对路径深度
  depth=$(dirname "$f" | tr '/' '\n' | grep -c .)
  prefix="../".repeat(depth)

  # 注入 CSS 到 </head> 前
  sed -i "s|</head>|  <link rel=\"stylesheet\" href=\"${prefix}_shared/home-button.css\">\n</head>|" "$f"

  # 注入 JS 到 </body> 前
  sed -i "s|</body>|  <script src=\"${prefix}_shared/home-button.js\"></script>\n</body>|" "$f"
done
```

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
| 入学篇 | 1-13话 | ~12 |
| 住宿研修 | 14-27话 | ~20 |
| 秋季选拔 | 28-60话 | ~23 |
| 食戟vs久我 | 61-87话 | ~16 |
| 实习篇 | 88-106话 | ~11 |
| 月飨祭 | 107-137话 | ~17 |
| 远月列车 | 138-158话 | ~10 |
| 联队食戟 | 159-217话 | ~29 |
| THE BLUE | 218-315话 | ~55 |
| 番外篇 | 3话 | ~5 |

**料理体系**：日式、法式、意式、中式、东南亚、分子美食学等
