# ACG 知识手册库

从动漫与游戏中发现真实世界的知识。

## 在线访问

https://your-username.github.io/acg-knowledge-handbook/

## 包含作品

| 作品 | 类型 | 内容 |
|------|------|------|
| [魔王勇者](doc/maoyuu-politicalecon/) | 政治经济学手册 | 小说内容 ↔ 学术著作 ↔ 历史事件 三方对照 |
| [食戟之灵](doc/shokugeki-no-soma/) | 料理全鉴 | 全315话逐章详解260+道料理 |

## 目录结构

```
.
├── index.html                  # 项目主页（落地页）
├── .nojekyll                   # 禁用 Jekyll 处理
├── _shared/                    # 项目级共享资源
│   ├── style.css               # 主页样式
│   ├── home-button.css         # 主页按钮样式
│   ├── home-button.js          # 主页按钮注入脚本
│   └── fonts/                  # 字体文件
├── doc/                        # 作品内容目录
│   ├── maoyuu-politicalecon/   # 魔王勇者
│   └── shokugeki-no-soma/      # 食戟之灵
└── .github/workflows/
    └── deploy.yml              # GitHub Actions 部署工作流
```

## 添加新作品

1. 将作品 HTML 文件夹放入 `doc/作品英文名/`
2. 在 `index.html` 的「作品知识手册」区域添加作品卡片
3. 推送至 GitHub，自动部署

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

## 免责声明

本站为粉丝自发整理的非官方内容。所有资料基于原作及公开学术资源整理，仅供学习交流使用。作品版权归原作者及出版社所有。
