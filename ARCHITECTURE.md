# 项目架构文档

> 面向维护者与贡献者，说明当前仓库如何组织首页、数据源、统一脚本与部署流程。

---

## 1. 架构目标

当前架构只围绕五个目标设计：

1. **首页可维护**：首页由数据生成，而不是手工长期维护
2. **接入成本低**：新增手册时尽量只需放目录并登记最少信息
3. **手册独立**：不强行统一各手册内部结构
4. **项目级能力集中**：校验、统计、注入、部署统一放在项目级层面处理
5. **容错优先**：缺失字段优先通过兜底逻辑容错，而不是直接阻断接入

---

## 2. 结构总览

```text
.
├── index.html                      # 生成后的项目首页
├── README.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── _data/
│   ├── homepage-data.json          # 首页通用文案 / 区块配置
│   ├── handbooks.json              # 手册注册表
│   └── project-metrics.json        # 自动生成的项目级统计摘要
├── _shared/
│   ├── homepage.css                # 首页样式
│   ├── homepage.js                 # 首页交互
│   ├── home-button.css             # 统一返回首页按钮样式
│   └── home-button.js              # 统一返回首页按钮脚本
├── doc/
│   └── <folder>/                   # 各手册目录
│       ├── index.html              # 对应手册主页
│       ├── ...其他页面...
│       └── _shared/                # 该手册自己的样式 / 脚本
├── scripts/
│   ├── project_tools.py            # 项目级统一工具入口
│   └── project_tools_lib/          # 内部按职责拆分的实现模块
└── .github/workflows/
    └── deploy.yml                  # 校验、生成、注入、部署
```

---

## 3. 三层模型

### 3.1 首页层
负责：

- 首页展示
- 作品索引
- 知识地图
- 阅读路径
- 筛选交互
- 项目说明
- 自动统计展示

核心文件：

- `index.html`
- `_data/homepage-data.json`
- `_data/handbooks.json`
- `_data/project-metrics.json`
- `_shared/homepage.css`
- `_shared/homepage.js`

### 3.2 手册层
负责：

- 单个手册的实际内容页面
- 单个手册自己的样式、脚本与结构

核心路径：

- `doc/<folder>/`

项目级优化默认不修改这一层。

### 3.3 部署层
负责：

- 项目级校验
- 首页与统计摘要生成
- 返回首页按钮注入
- GitHub Pages 部署

核心文件：

- `.github/workflows/deploy.yml`
- `_shared/home-button.css`
- `_shared/home-button.js`
- `scripts/project_tools.py`

---

## 4. 数据流

### 4.1 首页数据源

#### `_data/homepage-data.json`
负责：

- 首页公共文案
- 区块标题与说明
- 知识领域定义
- 筛选器定义
- 阅读路径与方法说明

#### `_data/handbooks.json`
负责：

- 当前有哪些手册被接入首页系统
- 每个手册的最小注册信息
- 每个手册可选的展示补充字段

#### `_data/project-metrics.json`
负责：

- 自动生成的项目级统计摘要
- 供首页展示与维护检查使用

### 4.2 生成流

```text
homepage-data.json + handbooks.json + doc/<folder>/*.html
                ↓
        project_tools.py generate
                ↓
      index.html + project-metrics.json
```

### 4.3 自动推导内容

当前会自动推导：

- 手册总数
- 页面总数
- 领域数量
- 内容页 / 辅助页统计
- 各领域页面分布
- 各媒介分布
- 待归类手册数量
- 使用兜底媒介的手册数量
- 缺省展示字段的兜底文案

---

## 5. 统一工具脚本

当前项目级 Python 工具对外只保留一个统一入口：

- `scripts/project_tools.py`

但内部已经按职责拆分到：

- `scripts/project_tools_lib/homepage.py`
- `scripts/project_tools_lib/checks.py`
- `scripts/project_tools_lib/buttons.py`
- `scripts/project_tools_lib/registry.py`
- `scripts/project_tools_lib/common.py`

### 默认入口

```bash
python scripts/project_tools.py
```

在终端环境下会进入交互式菜单；如果没有交互式终端环境，则默认执行：

```bash
python scripts/project_tools.py verify
```

### 子命令

```bash
python scripts/project_tools.py menu
python scripts/project_tools.py verify
python scripts/project_tools.py validate
python scripts/project_tools.py generate
python scripts/project_tools.py check-links
python scripts/project_tools.py inject-home-buttons
python scripts/project_tools.py strip-home-buttons
python scripts/project_tools.py check-home-buttons
python scripts/project_tools.py list-handbooks
python scripts/project_tools.py add-handbook
python scripts/project_tools.py edit-handbook
python scripts/project_tools.py remove-handbook
```

### 职责

#### `verify`
串联执行：

1. 注册表校验
2. 首页生成
3. 链接检查
4. 返回首页按钮状态检查

这是**本地维护与 CI 的统一入口**。

#### `validate`
负责：

- 校验 `_data/handbooks.json` 结构
- 校验 `doc/<folder>/` 是否存在
- 校验 `doc/<folder>/index.html` 是否存在
- 检查重复 `folder`
- 检查 `domain` / `medium` 是否缺失或未预定义
- 验证首页是否可成功生成

#### `generate`
负责：

- 扫描 `doc/<folder>/*.html`
- 生成首页
- 生成统计摘要
- 自动应用 `domain` / `medium` 兜底逻辑
- 自动推导 `scale / structure / startHere` 默认值

#### `check-links`
负责：

- 检查项目级 Markdown 文档中的本地链接
- 检查生成后的首页本地链接
- 检查 `doc/` 下 HTML 页面中的本地 `href / src`

#### `inject-home-buttons`
负责：

- 给 `doc/**/*.html` 页面注入统一返回首页按钮依赖
- 自动写入正确的 `data-home-href`
- 支持幂等执行
- 规范化旧标签
- 注入后立即校验结果

---

## 6. 新增手册接入模型

当前系统目标是：

> 新增手册时，不需要手改首页 HTML，也不需要为每个手册额外接入项目级组件。

### 最低接入要求

1. `doc/<folder>/index.html` 存在
2. `_data/handbooks.json` 中新增一条记录

### 最低记录示例

```json
{
  "folder": "new-work-folder",
  "title": "新作品名"
}
```

### 字段分层

#### 必填字段

- `folder`
- `title`

#### 常用推荐字段

- `subtitle`
- `domains`
- `medium`
- `tags`
- `summary`
- `startHere`

#### 自动推导 / 可覆盖字段

- `scale`
- `structure`
- `href`
- `cta`

#### 保留字段

- `domainLabel`（当前首页未直接使用，一般无需填写）

其中：

- `domains` 推荐写成数组，适合一个作品同时对应多个知识领域
- `medium` 也推荐写成数组，适合一个作品同时对应小说 / 漫画 / 动画 / 游戏等多种媒介
- `href` 用于覆盖默认入口地址；不填时默认使用 `doc/<folder>/index.html`
- `cta` 用于覆盖首页卡片底部入口文案

### 自动兜底策略

#### `domain / domains` 缺失或非法
自动回落到：
- `uncategorized / 待归类`

#### `medium` 缺失或非法
自动回落到：
- `other / 其他`

#### `scale / structure / startHere` 缺失
根据目录下页面结构自动生成默认说明。

#### `href / cta` 缺失
分别回落到默认入口地址和默认入口文案。

---

## 7. 统一返回首页按钮

这是当前唯一明确要求“全站统一”的跨手册组件。

### 目标
部署后所有手册页面都应拥有：

- 完全相同的返回首页按钮
- 完全一致的样式与行为
- 正确的首页跳转路径

### 原则
- 不手工逐页维护按钮标签
- 不要求每个手册自己设计不同版本的返回按钮
- 本地可以先通过统一工具把标签写入源码
- CI 部署前会再次执行幂等注入，并继续做状态校验

### 注入方式
工作流调用：

```bash
python scripts/project_tools.py inject-home-buttons
```

处理范围：

```text
doc/**/*.html
```

写入内容：

- `<link rel="stylesheet" href=".../_shared/home-button.css">`
- `<script src=".../_shared/home-button.js" data-home-href=".../index.html"></script>`

### 当前增强点
- 幂等注入
- 旧标签规范化
- 注入后校验
- 结果汇总输出

---

## 8. GitHub Pages 部署流程

当前部署流程：

```text
Checkout
  ↓
Inject shared home button into handbook pages
  ↓
Verify project
  ↓
Upload Pages artifact
  ↓
Deploy to GitHub Pages
```

### 工作流负责
1. 以幂等方式把返回首页按钮统一收敛到标准状态
2. 通过统一入口完成项目级校验（含按钮状态检查）
3. 部署静态站点

### 工作流不负责
1. 不修改手册内部内容
2. 不重写手册自己的样式
3. 不给每个手册注入复杂项目级 UI

---

## 9. 维护边界

### 可以改的
- `index.html`（通常由生成器生成）
- `_data/` 下的首页数据、手册注册表、统计摘要
- `_shared/homepage.*`
- `_shared/home-button.*`
- `scripts/project_tools.py`
- `.github/workflows/deploy.yml`
- 项目级说明文档

### 默认不改的
- `doc/<folder>/` 下每个手册的内部内容
- 每个手册自己的 `_shared/style.css` / `script.js`
- 已经完成且用户满意的手册页面结构

---

## 10. 当前状态与后续方向

当前主计划项已经完成，项目级基础设施处于可用状态。

如果后续仍要继续优化，更适合从这些可选方向切入：

- 首页展示层的进一步轻量打磨
- CI 输出与日志友好性增强
- 项目级文档的细节可读性微调
- 在不增加接入成本的前提下继续减少重复维护

