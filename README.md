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

然后访问 `http://localhost:8000` 或直接打开 `index.html`

## 🛠️ 技术栈

- **前端**: 纯静态 HTML / CSS / JavaScript
- **托管**: GitHub Pages
- **部署**: GitHub Actions 自动部署
- **字体**: Google Fonts CDN
- **图表**: ECharts CDN
- **流程图**: Mermaid CDN

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
├── content/                    # 内容页面
│   ├── dr-stone-science/      # 《石纪元》项目
│   │   └── index.html
│   ├── maoyuu-political-economy/  # 《魔王勇者》项目
│   │   └── index.html
│   ├── shokugeki-no-soma/     # 《食戟之灵》项目
│   │   ├── index.html
│   │   └── arc-*.html
│   └── tondemo-skill-food/    # 异世界流浪美食家项目
│       └── index.html
├── scripts/                    # JavaScript 脚本
│   └── navigation.js
├── styles/                     # CSS 样式
│   └── base.css
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
| `content/` | 各作品的内容页面（HTML） |
| `scripts/` | 共享 JavaScript 脚本 |
| `styles/` | 共享 CSS 样式 |

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

### 添加新作品

1. 在 `content/` 下创建新的子项目目录
2. 在 `assets/images/` 下创建对应的图片资源目录
3. 添加HTML页面和资源文件
4. 在主 `index.html` 中添加导航链接
5. 更新 README.md 项目列表

### 更新现有作品

1. 修改对应子项目的HTML文件
2. 更新图片资源(如需)
3. 推送更改到GitHub,自动部署

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
3. 添加新作品内容
4. 提交更改 (`git commit -m "Add: 新作品XXX"`)
5. 推送到分支 (`git push origin feature/new-work`)
6. 创建Pull Request

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

**最后更新**: 2026-06-14