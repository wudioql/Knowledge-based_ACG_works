# ACG 知识手册库

[![Deploy](https://github.com/wudioql/Knowledge-based_ACG_works/actions/workflows/deploy.yml/badge.svg)](https://github.com/wudioql/Knowledge-based_ACG_works/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://wudioql.github.io/Knowledge-based_ACG_works/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> 从动漫与游戏中挖掘真实世界知识，建立「**虚构作品内容 ↔ 学术理论 ↔ 真实历史**」的三方对照体系。

---

## 项目概览

### 核心理念

本项目试图回答一个问题：**一部优秀的 ACG 作品，除了娱乐价值，还能带给我们什么？**

许多作品在虚构叙事中融入了真实的知识体系——经济学原理、政治制度、料理科学、历史事件。本项目将这些隐藏的知识脉络梳理出来，建立三方对照，让作品成为通往真实知识世界的入口。

```mermaid
graph LR
    A[虚构作品内容] --> B[学术理论]
    A --> C[真实历史]
    B --> C
```

### 设计哲学：一作一貌

本项目坚持「**一作一貌**」的设计理念：**每部 ACG 作品的知识手册都应拥有独立的视觉个性，反映原作的内容气质。** 我们刻意避免所有作品共用同一套页面骨架、字体组合与布局模式。

> ⚠️ **现状提示**：目前的两部作品（《魔王勇者》《食戟之灵》）在页面骨架、字体与脚本结构上仍较为相似，属于早期遗留。新增作品时**必须**与所有已有作品做出显著区分，详见 [CONTRIBUTING.md — 视觉身份差异化指南](./CONTRIBUTING.md#视觉身份差异化指南)。

### 在线访问

**[https://wudioql.github.io/Knowledge-based_ACG_works/](https://wudioql.github.io/Knowledge-based_ACG_works/)**

---

## 作品总览

| 作品 | 知识领域 | 内容类型 | 视觉风格 | 状态 |
|------|----------|----------|----------|------|
| [魔王勇者](./doc/maoyuu/) | 政治经济学 | 手册 | 学术冷色调 · 暗红 #8B0000 · 卷卡网格 + 左侧 TOC | 已完成 |
| [食戟之灵](./doc/shokugeki_no_soma/) | 料理学 | 全鉴 | 料理暖色调 · 亮红 #C0392B · 篇章卡片 + 右侧 TOC | 已完成 |
| *(预留)* | | | | |

> 新作品添加后，请在 [CONTRIBUTING.md — 已有作品视觉档案](./CONTRIBUTING.md#已有作品视觉档案) 中登记其视觉指纹，便于后续贡献者比对差异化。

---

## 快速开始

### 在线浏览

直接访问 **[GitHub Pages 站点](https://wudioql.github.io/Knowledge-based_ACG_works/)** 即可，无需安装任何依赖。

### 本地预览

```bash
git clone https://github.com/wudioql/Knowledge-based_ACG_works.git
cd Knowledge-based_ACG_works
# 任选其一：
python3 -m http.server 8080   # 推荐：保持相对路径行为与线上一致
# 或直接用浏览器打开 index.html
```

> 本项目为**纯静态网站**：HTML + CSS + JavaScript，**零运行时依赖**（无 npm、无框架、无打包器），且**无需本地构建工具链**。
> 唯一的"构建"动作是 CI 在部署期自动注入"返回主页"按钮（一段轻量 `find + sed` 处理，见 [ARCHITECTURE.md — 构建与部署流程](./ARCHITECTURE.md#5-构建与部署流程)）。内容页面本身无需任何构建即可浏览；因此本地直接打开作品页时不会出现该按钮，但**基本不影响**内容阅读（无法回到首页以切换作品，仅可回退至首页再切换）。本地预览推荐用下面的静态服务器，以保证相对路径与字体加载行为与线上一致。

---

## 项目特性

- **三方对照体系**：每部作品的内容都与学术理论和真实历史建立对照
- **一作一貌**：每部作品拥有独立视觉设计，反映原作气质（强约束，见 CONTRIBUTING）
- **纯静态架构**：HTML + CSS + Vanilla JS，无框架、无构建工具，长期可维护
- **在线字体策略**：字体一律通过 Google Fonts 在线引入，**不使用本地字体文件**
- **内容拆分**：按章节 / 卷 / 篇章拆分为独立 HTML 文件，保持单文件可控
- **知识可视化**：合理运用 ECharts / Mermaid / SVG.js（均在线 CDN 引入）优化知识呈现
- **全局返回按钮**：`_shared/` 在构建时自动为所有非首页页面注入「返回主页」按钮，**作品手册编写时无需关心**
- **自动部署**：推送至 GitHub 后自动部署到 GitHub Pages
- **响应式设计**：适配桌面端与移动端

---

## 技术架构（概览）

| 类别 | 技术 | 说明 |
|------|------|------|
| 页面结构 | HTML5 | 语义化标签，无框架 |
| 样式 | CSS3 | CSS 变量 + 原生选择器，无预处理器 |
| 交互 | Vanilla JavaScript | IIFE 封装，无框架 |
| 字体 | Google Fonts（在线引入） | 每部作品独立选择，参见 [字体政策](./CONTRIBUTING.md#字体政策) |
| 可视化 | ECharts / Mermaid / SVG.js（在线 CDN） | 参见 [可视化规范](./CONTRIBUTING.md#可视化规范) |
| 部署 | GitHub Actions + GitHub Pages | 推送即部署 |

> 完整的架构图、模块职责、关键函数说明、依赖关系与运行方式，请参阅 **[ARCHITECTURE.md](./ARCHITECTURE.md)**。

---

## 内容体系

### 按知识领域分类

| 领域 | 现有作品 | 潜在方向 |
|------|----------|----------|
| 政治经济学 | 魔王勇者 | 国际关系、制度经济学、博弈论 |
| 料理科学 | 食戟之灵 | 食品化学、营养学 |
| 历史学 | — | 军事史、科技史 |
| 自然科学 | — | 物理学、生物学 |

### 按内容类型分类

| 类型 | 说明 | 推荐视觉模式 | 示例 |
|------|------|--------------|------|
| 手册 | 按章节系统梳理知识点，附学术对照 | 学术风格，双栏对照表，侧边目录 | 魔王勇者 |
| 全鉴 | 逐条目详解，附技术拆解 | 图文并茂，卡片流，沉浸式排版 | 食戟之灵 |
| 年表 | 按时间线整理事件与史实对照 | 垂直时间线，节点式布局 | *(预留)* |
| 地图 | 地理设定与真实地理 / 历史对照 | 交互式地图，标注式信息卡 | *(预留)* |

---

## 参与贡献

欢迎提交新的 ACG 知识整理！无论是新增作品、补充现有内容，还是修正错误：

- **提交 Issue**：报告内容错误或提出新作品建议
- **提交 Pull Request**：按 [添加新作品指南](./CONTRIBUTING.md#添加新作品指南) 操作
- **内容讨论**：在 Issue 区讨论知识点的准确性与深度

> **重要**：添加新作品前，**务必**阅读 [视觉身份差异化指南](./CONTRIBUTING.md#视觉身份差异化指南)，确保新作品的视觉设计与已有作品存在**显著差异**。

---

## 文档导航

| 文档 | 面向读者 | 说明 |
|------|----------|------|
| [README.md](./README.md) | 所有人 | 项目概览与设计哲学（本文档） |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 开发者 / 维护者 | 项目架构、模块职责、关键函数、依赖关系、运行方式 |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 贡献者 / 开发者 | 开发规范、差异化指南、字体 / 拆分 / 可视化政策、新增作品流程 |

> 此外，项目在 GitHub 上设有独立的 **Wiki**，承载方法论、教程、资源等长青内容（与仓库内文档分工见 Wiki 首页说明）。

---

## 许可证与免责声明

本项目采用 [MIT License](./LICENSE) 开源。

本站为粉丝自发整理的非官方内容。所有资料基于原作及公开学术资源整理，仅供学习交流使用。作品版权归原作者及出版社所有。
