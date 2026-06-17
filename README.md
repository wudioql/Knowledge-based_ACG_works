# ACG 知识手册库

从动漫与游戏中发现真实世界的知识。

## 在线访问

https://your-username.github.io/acg-knowledge-handbook/

## 包含作品

| 作品 | 类型 | 内容 |
|------|------|------|
| [魔王勇者](doc/maoyuu/index.html) | 政治经济学手册 | 小说内容 ↔ 学术著作 ↔ 历史事件 三方对照 |
| [食戟之灵](doc/shokugeki_no_soma/index.html) | 料理全鉴 | 全315话逐章详解260+道料理 |

## 文档

- [项目结构规范 (CODE_WIKI)](docs/CODE_WIKI.md) — 完整的架构、模块、依赖关系文档
- 本 README — 快速入门和部署指南

## 目录结构

```
.
├── index.html                  # 项目主页（落地页）
├── .nojekyll                  # 禁用 Jekyll 处理
├── _shared/                    # 项目级共享资源
│   ├── style.css               # 主页样式
│   ├── home-button.css         # 主页按钮样式
│   └── home-button.js          # 主页按钮注入脚本
├── doc/                        # 作品内容目录
│   ├── maoyuu/                 # 魔王勇者
│   │   ├── index.html          # 作品首页
│   │   ├── vol-*.html          # 各卷知识点内容（8卷+番外）
│   │   ├── glossary.html       # 术语表
│   │   ├── references.html     # 参考文献
│   │   └── _shared/            # 作品级共享资源
│   │       ├── style.css      # 作品样式表
│   │       └── script.js       # 作品交互脚本
│   └── shokugeki_no_soma/      # 食戟之灵
│       ├── index.html          # 作品首页
│       ├── arc-*.html          # 各篇章料理内容（10个篇章）
│       └── _shared/            # 作品级共享资源
│           ├── style.css       # 作品样式表
│           └── script.js       # 作品交互脚本
├── docs/                       # 项目文档
│   └── CODE_WIKI.md           # 完整项目架构文档
└── .github/workflows/
    └── deploy.yml             # GitHub Actions 部署工作流
```

## 技术架构

| 类别 | 技术 |
|------|------|
| 页面结构 | HTML5（原生，无框架） |
| 样式 | CSS3（原生，无预处理器） |
| 交互 | Vanilla JavaScript（原生，无框架） |
| 字体 | Google Fonts (Lora, WorkSans) |
| 部署 | GitHub Actions + GitHub Pages |
| 托管 | GitHub Pages（静态托管） |

## 添加新作品

1. 将作品 HTML 文件夹放入 `doc/作品英文名/`
2. 创建 `doc/作品英文名/_shared/` 目录，包含 `style.css` 和 `script.js`
3. 在根 `index.html` 的「作品知识手册」区域添加作品卡片
4. 推送至 GitHub，自动部署

主页按钮会通过 GitHub Actions 工作流自动注入到所有 `doc/` 下的 HTML 页面中，无需手动修改作品源码。

## 本地预览

```bash
cd acg-knowledge-handbook
python3 -m http.server 8080
# 访问 http://localhost:8080
```

## 部署说明

本项目使用 GitHub Actions 自动部署到 GitHub Pages：

- 推送到 `main` 或 `master` 分支时自动触发部署
- 也可手动在 Actions 页面触发 `workflow_dispatch`
- 部署前工作流会自动为所有作品页面注入「主页」按钮

## 核心功能模块

### 主页 (`index.html`)
- 展示所有作品手册入口卡片
- 显示项目统计数据（作品数、知识点数、学科领域数）
- 包含 Hero 区域和 About 区域

### 主页按钮自动注入 (`_shared/home-button.js`)
- CI/CD 部署时自动注入到所有 `doc/` 下的 HTML 文件
- 根据 URL 深度动态计算返回主页的相对路径
- 固定定位圆形按钮，悬停显示"主页"标签

### 魔王勇者模块 (`doc/maoyuu/`)
- **知识点三方对照表**：小说内容 ↔ 学术理论 ↔ 历史事件
- **学科分类筛选**：经济学、政治学、历史学、技术、哲学
- **学者著作索引**：亚当·斯密、凯恩斯、熊彼特等16位学者
- **侧边目录导航**：滚动高亮当前阅读位置

### 食戟之灵模块 (`doc/shokugeki_no_soma/`)
- **料理卡片系统**：逐章详解260+道料理
- **料理体系分类**：日式、法式、意式、中式、分子美食学
- **烹饪技法索引**：球化、Confit、发酵、熏制等
- **动画对应表**：5季动画与漫画话数对应关系

## 免责声明

本站为粉丝自发整理的非官方内容。所有资料基于原作及公开学术资源整理，仅供学习交流使用。作品版权归原作者及出版社所有。
