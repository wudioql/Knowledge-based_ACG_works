# 贡献与维护指南

> 本文档只描述当前仓库真正需要的通用维护流程，不展开任何具体手册内容细节。

---

## 1. 适用范围

当前仓库的维护重点是：

1. **项目首页**
2. **项目级操作优化**
3. **新增手册的低成本接入**

默认原则：

- **不主动改动各手册内部内容**
- **不要求各手册统一改造成相同结构**
- **不要求新增手册手动接入复杂项目级组件**

如果你要修改的是：

- 首页
- `_data/` 数据源
- 生成脚本
- 部署工作流
- 项目级文档

那么这份文档适用。

如果你准备修改的是某个具体手册内部页面，请先确认那确实是必要行为，而不是项目级问题。

---

## 2. 新增手册的最简流程

### 第一步：放入手册目录

把新手册放到：

```text
doc/<folder>/
```

并确保至少存在：

```text
doc/<folder>/index.html
```

### 第二步：登记到 `_data/handbooks.json`

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
python scripts/project_tools.py verify
```

如果你想明确进入交互式菜单，而不是依赖环境判断，推荐使用：

```bash
python scripts/project_tools.py menu
```

其中：

- `inject-home-buttons`：把统一返回首页按钮写入所有手册页面源码
- 默认的 `project_tools.py`：在终端环境下会进入交互菜单
- 菜单中的新增 / 编辑 / 删除手册登记支持分组表单引导；编辑前会先打印当前登记信息预览，删除前也会先打印预览，再解释字段用途并提供 `domains` / `medium` 等输入示例
- 完成后还会询问是否立即执行后续推荐动作
- 每次操作结束后会先停在结果页，等你按回车再返回菜单，避免结果被完整菜单马上顶到上方
- 菜单还按“推荐工作流 / 手册登记管理 / 核心操作 / 按钮管理”分组展示
- 菜单提供“帮助 / 示例速查”入口，可随时查看推荐写法与工作流
- 如需跳过菜单，显式写成 `python scripts/project_tools.py verify`

### 第四步：本地检查后提交

建议至少检查：

- 首页是否生成成功
- 新作品是否出现在作品索引中
- 新作品入口是否正确

---

## 3. 手册注册字段字典

这一节可以把 `_data/handbooks.json` 理解成一个很轻量的“项目级注册接口”。

### 3.1 字段总表

| 字段 | 类型 | 是否必填 | 首页 / 工具中的用途 | 缺失时行为 | 建议 |
|---|---|---:|---|---|---|
| `folder` | `string` | 是 | 对应 `doc/<folder>/` 目录；也是默认入口路径的一部分 | 校验失败 | 必须与目录名一致 |
| `title` | `string` | 是 | 首页作品卡片主标题 | 校验失败 | 保持简洁稳定 |
| `subtitle` | `string` | 否 | 首页卡片副标题 | 回落到通用默认值 | 推荐填写 |
| `domains` | `string[]` | 否 | 知识地图归类、领域筛选、统计 | 回落到 `uncategorized / 待归类` | 推荐使用数组 |
| `medium` | `string[]` | 否 | 媒介筛选、统计 | 回落到 `other / 其他` | 推荐使用数组 |
| `tags` | `string[]` | 否 | 首页卡片标签提示 | 仅显示更少标签 | 推荐填写 3–6 个核心标签 |
| `summary` | `string` | 否 | 首页卡片摘要 | 回落到通用说明 | 推荐填写一句话概述 |
| `scale` | `string` | 否 | 卡片中的“规模”说明 | 按页面统计自动推导 | 只有想手动覆盖时再填 |
| `structure` | `string` | 否 | 卡片中的“结构亮点”说明 | 按目录结构自动推导 | 只有想手动覆盖时再填 |
| `startHere` | `string` | 否 | 卡片中的“从这里开始”阅读建议 | 自动生成通用引导文案 | 推荐填写 |
| `href` | `string` | 否 | 覆盖作品卡片入口地址 | 默认使用 `doc/<folder>/index.html` | 仅在默认入口不合适时填写 |
| `cta` | `string` | 否 | 覆盖卡片底部入口文案 | 自动生成“进入《标题》手册” | 仅在默认文案不合适时填写 |
| `domainLabel` | `string` | 否 | 保留字段 | 当前首页未直接使用 | 一般不要填写 |

### 3.2 字段分层理解

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

- `domainLabel`

### 3.3 最小示例

```json
{
  "folder": "new-work-folder",
  "title": "新作品名"
}
```

### 3.4 常用增强示例

```json
{
  "folder": "new-work-folder",
  "title": "新作品名",
  "subtitle": "知识手册",
  "domains": ["food", "micro"],
  "medium": ["manga", "anime"],
  "tags": ["示例标签 A", "示例标签 B"],
  "summary": "一句话说明该手册通向什么知识方向。",
  "scale": "共 12 个页面",
  "structure": "按主题整理 + 辅助页",
  "startHere": "先从手册首页总览开始。"
}
```

---

## 4. `domain` 与 `medium` 的建议值

### `domains`
当前首页支持更通用的知识领域分组，常用值包括：

- `life`
- `food`
- `micro`
- `society`
- `history`
- `space`

推荐写成数组，例如：

```json
"domains": ["food", "micro"]
```

如果不填写：
- 首页仍可生成
- 作品仍会进入索引
- 会自动落到“待归类”兜底分组中

### `medium`
当前首页把媒介统一收敛为四类：

- `novel`
- `manga`
- `anime`
- `game`

推荐写成数组，例如：

```json
"medium": ["manga"]
```

或：

```json
"medium": ["novel", "manga", "anime"]
```

---

## 5. 首页维护流程

### 5.1 首页文案与区块配置
维护文件：

- `_data/homepage-data.json`

适合修改的内容：

- Hero 文案
- 区块标题
- 知识领域说明
- 阅读路径
- 方法说明
- 页脚说明

### 5.2 手册列表与首页作品卡
维护文件：

- `_data/handbooks.json`

适合修改的内容：

- 新增手册
- 调整作品标题与摘要
- 补充 tags / summary / startHere 等字段

### 5.3 一次执行项目级校验与首页生成

```bash
python scripts/project_tools.py
```

在终端环境下它会打开交互式菜单；如果你想直接执行总校验，也可以显式写：

```bash
python scripts/project_tools.py verify
```

生成结果：

- `index.html`
- `_data/project-metrics.json`

如果你只想单独执行某一步，也可以分别运行：

```bash
python scripts/project_tools.py validate
python scripts/project_tools.py generate
python scripts/project_tools.py check-home-buttons
python scripts/project_tools.py check-links
python scripts/project_tools.py strip-home-buttons
python scripts/project_tools.py add-handbook
python scripts/project_tools.py edit-handbook
python scripts/project_tools.py remove-handbook
```

> 一般不要手改生成后的 `index.html`，优先回到数据源或生成器修改。

---

## 6. 返回首页按钮规则

所有 `doc/` 下的 HTML 页面都应带有统一的返回首页按钮，但当前约定是：

- **按钮标签可以先由本地工具统一写入源码**
- **CI 部署前会再次执行幂等注入，再校验按钮状态**

推荐本地同步命令：

```bash
python scripts/project_tools.py inject-home-buttons
```

如需恢复手册“未注入的初始状态”，可执行：

```bash
python scripts/project_tools.py strip-home-buttons
```

因此：

- 不要手工逐页维护这个按钮
- 不要给不同手册做不同版本的返回首页按钮
- 不要在手册内部复制项目级按钮逻辑

统一来源仍然是：

- `_shared/home-button.css`
- `_shared/home-button.js`
- `scripts/project_tools.py`

当前策略是：

- 本地可先注入到源码中，便于预览最终效果
- CI 部署前会再次执行注入
- 因为注入逻辑是幂等的，重复执行不会导致按钮标签不断叠加

---

## 7. 提交前最低检查

### 如果你改了首页数据
请检查：

- [ ] `python scripts/project_tools.py` 能成功执行
- [ ] 生成后的 `index.html` 可正常打开
- [ ] 首页中新增/修改的链接存在
- [ ] 作品索引与筛选没有明显错误

### 如果你改了部署工作流
请检查：

- [ ] 仍然会先执行项目级校验
- [ ] 仍然会注入统一返回首页按钮
- [ ] 重复执行不会无限重复注入标签
- [ ] 注入后仍然会再次检查本地链接
- [ ] 不会要求手册页手动改动
- [ ] 不会把首页生成与手册内部结构强耦合

---

## 8. 不推荐的做法

以下做法会增加未来维护成本，默认不建议：

- 手工直接改生成后的首页 HTML
- 为每个手册手动添加项目级返回按钮
- 要求新增手册必须接入统一头部 / 统一布局 / 统一组件
- 把首页逻辑写死在多个地方
- 为一个新手册新增过多必须字段，导致接入成本变高

项目的目标是：

> **新增手册时，最少只需要放文件夹并补一条登记信息。**

---

## 9. 推荐提交范围

### 合适的提交
- 更新首页文案
- 调整首页筛选与展示
- 新增手册注册表项
- 修复首页生成逻辑
- 优化部署工作流
- 更新项目说明文档

### 默认不应混在一起的提交
- 首页工程化优化
- 某个手册内部内容重写
- 某个手册的独立视觉大改

除非明确需要，否则项目级修改与手册内部修改应尽量分离。

---

## 10. 文档与脚本入口

项目级维护常用入口：

- `README.md`
- `ARCHITECTURE.md`
- `CONTRIBUTING.md`
- `_data/homepage-data.json`
- `_data/handbooks.json`
- `scripts/project_tools.py`
- `.github/workflows/deploy.yml`

如果你不确定应该改哪里，优先从这几处开始，而不是直接改手册内部页面。
