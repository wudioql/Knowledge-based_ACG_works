# ACG 知识手册库

[![Deploy](https://github.com/wudioql/Knowledge-based_ACG_works/actions/workflows/deploy.yml/badge.svg)](https://github.com/wudioql/Knowledge-based_ACG_works/actions/workflows/deploy.yml)

一个以 **ACG 作品为入口、以现实知识为主轴** 的纯静态手册项目。

当前仓库的项目级维护目标只有三件事：

1. **首页可维护**：首页由数据生成，而不是手工长期维护
2. **接入成本低**：新增手册时尽量只需放目录并登记最少信息
3. **不打扰手册内部**：项目级优化默认不改各手册内部页面

---

## 当前边界

项目级层面负责：

- 首页展示
- 手册注册表
- 项目级统计摘要
- 统一返回首页按钮
- 校验、生成、部署流程
- 项目级文档

默认不负责：

- `doc/<folder>/` 下各手册内部内容
- 各手册自己的样式、脚本与结构改造

---

## 目录结构

```text
.
├── index.html                      # 生成后的项目首页
├── _data/
│   ├── homepage-data.json          # 首页通用文案与配置
│   ├── handbooks.json              # 手册注册表
│   └── project-metrics.json        # 自动生成的项目级统计摘要
├── _shared/
│   ├── homepage.css                # 首页样式
│   ├── homepage.js                 # 首页交互
│   ├── home-button.css             # 统一返回首页按钮样式
│   └── home-button.js              # 统一返回首页按钮脚本
├── doc/                            # 所有手册目录
│   └── <folder>/                   # 各手册目录
│       ├── index.html              # 对应手册主页
│       ├── ...其他页面...
│       └── _shared/                # 该手册自己的样式 / 脚本
├── scripts/
│   └── project_tools.py            # 项目级统一工具入口
│   └── project_tools_lib/          # 内部按职责拆分的实现模块
└── .github/workflows/
    └── deploy.yml                  # 校验、生成、注入、部署
```

---

## 本地使用

### 预览

```bash
git clone https://github.com/wudioql/Knowledge-based_ACG_works.git
cd Knowledge-based_ACG_works
python3 -m http.server 8080
```

然后访问：

```text
http://localhost:8080
```

### 项目级校验与生成

如果你直接运行：

```bash
python scripts/project_tools.py
```

在终端环境下会进入一个**交互式菜单**。如果你希望明确打开菜单、避免环境判断差异，推荐直接运行：

```bash
python scripts/project_tools.py menu
```

如果你明确只想执行项目级总校验，而不是进入菜单，推荐直接运行：

```bash
python scripts/project_tools.py verify
```

可以直接选择：

- 校验项目
- 生成首页
- 注入 / 移除 / 检查返回首页按钮
- 列出、新增、编辑、删除手册登记信息

在新增 / 编辑手册登记时，菜单还会：

- 按“必填 / 常用展示 / 自动推导 / 保留字段”分组显示表单
- 编辑前先打印当前登记信息预览，便于对照后再修改
- 删除前也会先打印同样的预览，降低误删风险
- 显示当前可用领域与媒介选项
- 直接给出各字段的用途说明与常见输入示例
- 提示哪些字段可以留空
- 在编辑时区分“保留当前值”和“清空字段”
- 完成后提示建议的下一步校验命令
- 询问是否立即执行推荐流程（如注入按钮 + 总校验）
- 每次操作结束后会停在结果页，等待你按回车再返回菜单，避免输出被新菜单立刻刷走
- 菜单按“推荐工作流 / 手册登记管理 / 核心操作 / 按钮管理”分组展示
- 菜单首页直接展示推荐工作流入口（最常用的是“同步按钮并总校验”）
- 还提供“帮助 / 示例速查”，便于快速查看字段示例与常用流程

推荐日常流程仍然是：

```bash
python scripts/project_tools.py inject-home-buttons
python scripts/project_tools.py
```

其中：

- `inject-home-buttons`：把统一返回首页按钮写入所有手册页面源码
- 默认的 `project_tools.py`：在交互式终端中会进入菜单；在非交互环境下会自动切换到 `verify`
- `verify`：执行注册表校验、首页生成、按钮状态检查和本地链接检查

并更新：

- `index.html`
- `_data/project-metrics.json`

如需单独执行某一步：

```bash
python scripts/project_tools.py validate
python scripts/project_tools.py generate
python scripts/project_tools.py check-home-buttons
python scripts/project_tools.py check-links
python scripts/project_tools.py strip-home-buttons
```

---

## 新增手册的最低成本流程

### 第一步：放入手册目录

```text
doc/<folder>/index.html
```

### 第二步：在 `_data/handbooks.json` 追加记录

最低可用写法：

```json
{
  "folder": "new-work-folder",
  "title": "新作品名"
}
```

### 第三步：同步返回首页按钮并执行项目级校验

```bash
python scripts/project_tools.py inject-home-buttons
python scripts/project_tools.py
```

如果通过，这个手册就会：

- 出现在首页索引中
- 在源码中带上统一的返回首页按钮
- 在部署时直接通过按钮状态校验

> 推荐把 `domains` 和 `medium` 写成数组形式，这样一个作品可以同时对应多种媒介和多个知识领域；但它们都不是强制字段。

### 手册注册字段字典

下表只说明 `_data/handbooks.json` 中项目级会识别的常用字段：

| 字段 | 类型 | 是否必填 | 作用 | 缺失时行为 |
|---|---|---:|---|---|
| `folder` | string | 是 | 对应 `doc/<folder>/` 目录名 | 缺失会导致注册表校验失败 |
| `title` | string | 是 | 首页作品卡片主标题 | 缺失会导致注册表校验失败 |
| `subtitle` | string | 否 | 首页卡片副标题 | 回落到通用默认值 |
| `domains` | string[] | 否 | 知识领域归类；支持多领域 | 回落到 `uncategorized / 待归类` |
| `medium` | string[] | 否 | 媒介归类；支持多媒介筛选 | 回落到 `other / 其他` |
| `tags` | string[] | 否 | 首页卡片标签 | 留空时只显示媒介标签或更少标签 |
| `summary` | string | 否 | 首页卡片摘要 | 回落到通用默认说明 |
| `scale` | string | 否 | 卡片中的“规模”说明 | 按页面数量自动推导 |
| `structure` | string | 否 | 卡片中的“结构亮点”说明 | 按目录结构自动推导 |
| `startHere` | string | 否 | 卡片中的“从这里开始”阅读建议 | 自动生成通用引导文案 |
| `href` | string | 否 | 覆盖默认入口地址 | 默认使用 `doc/<folder>/index.html` |
| `cta` | string | 否 | 覆盖卡片底部入口文案 | 自动生成“进入《标题》手册” |
| `domainLabel` | string | 否 | 保留字段 | 当前首页未直接使用，一般无需填写 |

更完整的字段说明与录入建议见：

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 部署行为

GitHub Pages 工作流会自动完成：

1. 项目级校验
2. GitHub Pages 部署

也就是说，当前约定是：

- 统一返回首页按钮**作为源码的一部分保存在手册页面中**
- 本地可先注入再预览，确认最终效果
- CI 会在部署前再次执行注入，但注入逻辑是幂等的，不会无限重复写入同一标签
- CI 随后会继续检查按钮状态、首页生成结果和本地链接状态

这样既保留了本地预览最终效果的能力，也保证了部署前能统一收敛到标准状态。

---

## 文档分工

- [ARCHITECTURE.md](./ARCHITECTURE.md)：结构、数据流、部署流、维护边界
- [CONTRIBUTING.md](./CONTRIBUTING.md)：接入与修改流程

---

## 说明

本仓库中的手册内容为非官方整理，供学习与交流使用；相关作品版权归原作者、出版社及相关权利方所有。
