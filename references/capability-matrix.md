# 能力矩阵（capability-matrix）

> 把 Claude 当前会话能调用的所有能力，**按 6 大维度**整理成一张表。
> 路由时按这张表查。

## 1. 类比思维（analogy）

| 子能力 | 适用场景 | 工具/Skill | 限制 |
|---|---|---|---|
| 修仙类比 | 任何决策/事件的启发视角 | `xiuxian` skill（凡人修仙传 730 万字） | 类比≠真实知识 |
| 灵宝类比 | 工具/人物/思想的"灵宝化方案" | `lingbao-analyzer` skill（12 要素） | 不适合简单工具 |
| 一般比喻 | 抽象概念翻译 | Claude 本职 | 中学生口吻 |

**触发词**："按凡人修仙传看 X"、"灵宝化 X"、"打个比方"

## 2. 信息检索（research）

| 子能力 | 适用场景 | 工具 | 限制 |
|---|---|---|---|
| Web 搜索 | 任何事实查询 | `WebSearch` | 结果需二次核验 |
| 网页抓取 | 读 GitHub README / 文章 / 文档 | `WebFetch` | 截断风险（>20 页 PDF 失败） |
| 本地代码搜索 | 找符号/定义/用法 | `Grep` / `Glob` | 已知文件名更快 |
| GitHub 检索 | 查项目/PR/issue | `gh CLI` | 国内需 gh-proxy 镜像 |

**触发词**："搜索 X"、"查 X"、"X 是什么"、"GitHub 上有没有 X"

## 3. 代码生成（code）

| 子能力 | 适用场景 | 工具 | 限制 |
|---|---|---|---|
| 写代码 | 任何编程语言 | Claude 本职 | 重要代码需测试 |
| 跑脚本 | 执行 shell / python / node | `Bash` | 长任务用 run_in_background |
| Git 操作 | commit / push / 分支 | `Bash` (git) | push 前必须 ls-remote 核对 |
| GitHub 操作 | repo 创建/PR/issue | `gh CLI` | Windows 上要先 unset GITHUB_TOKEN |

**触发词**："写一个 X"、"用 X 语言实现 Y"、"跑一下 X"

## 4. 文档处理（document）

| 子能力 | 适用场景 | 工具 | 限制 |
|---|---|---|---|
| 读文件 | 任意文本/代码/PDF/图片/Jupyter | `Read` | 大文件用 offset/limit |
| 写文件 | 新建/覆盖 | `Write` | 覆盖前必须先 Read |
| 编辑文件 | 局部修改 | `Edit` | old_string 必须唯一 |
| Jupyter | 单元格编辑/运行 | `NotebookEdit` | 需 .ipynb 文件 |
| 路径搜索 | 找文件位置 | `Glob` / `Bash` (find) | Windows 上 find 用 Git Bash |

**触发词**："读 X 文件"、"写 X 文件"、"改 X 的 Y 段"

## 5. 并行调度（orchestration）

| 子能力 | 适用场景 | 工具 | 限制 |
|---|---|---|---|
| 单子任务 | 独立调研/写作 | `Agent` | 不可与主会话共享状态 |
| 多 agent 并行 | 多维度同时审查 | `Workflow` + `parallel()` | 同步屏障慢 |
| 流水线 | 找 → 审 → 改 → 验 | `Workflow` + `pipeline()` | 默认模式 |
| 子agent 隔离 | 并行写代码不冲突 | `Agent` + `isolation: worktree` | 贵 (~200-500ms/agent) |
| Plan 模式 | 先规划再实现 | `EnterPlanMode` / `ExitPlanMode` | 复杂任务才用 |
| 询问用户 | 卡住时获取偏好 | `AskUserQuestion` | 1-4 题，多选支持 |

**触发词**："并行做 X"、"用多 agent"、"先规划"、"先问 X"

## 6. 持久化（persistence）

| 子能力 | 适用场景 | 工具 | 限制 |
|---|---|---|---|
| 跨会话记忆 | 用户偏好/项目背景 | `memory/*.md` | 手动写文件 |
| 定时任务 | 每天/每小时提醒 | `CronCreate` / `CronDelete` / `CronList` | 仅 7 天有效 |
| 自节奏循环 | /loop 模式 | `ScheduleWakeup` | 仅动态模式 |
| 长任务心跳 | 等 CI/部署完成 | `ScheduleWakeup` 120-1800s | 不要 300s（worst case） |
| 会话间消息 | 通知其他 agent 空闲 | `SendMessage` + `notify_when_idle` | 仅本机 session |

**触发词**："每天 X 点提醒 Y"、"记住 X"、"等 X 完成后通知我"

## 跨能力组合（combo）

| 组合 | 场景 | 典型路径 |
|---|---|---|
| 类比 + 检索 | 给名人做灵宝分析 | xiuxian 类比 + WebSearch 搜资料 + lingbao-analyzer 归档 |
| 检索 + 文档 | 查 API 后写文档 | WebFetch 官方文档 → Read 现有 → Write 新文档 |
| 代码 + 测试 + 推送 | 完整开发循环 | Claude 写代码 → Bash 跑测试 → git push → gh repo view 核验 |
| 调度 + 持久化 | 每日多 agent 监控 | CronCreate → Workflow 多维分析 → memory 记录结果 |
| 类比 + 决策 | 投资/创业启发 | xiuxian 类比 → 检索真实数据 → 列出风险点 |

## 边界（不在矩阵内）

| 不能做 | 原因 |
|---|---|
| 物理世界操作 | 无机器人接口 |
| 24/7 持续在线 | 单次会话有上下文限制 |
| 100% 准确 | 幻觉存在，重要决策双重核对 |
| 承担法律责任 | 签字/合同主体是你 |
| 医疗/法律最终决策权 | 建议可以，决定是你的 |

## 一句话

**xiuxian 解决"想什么"，AI 工具解决"怎么做"，持久化解决"不忘事"，并行解决"加快"**——
四者叠加，在"坐在电脑前能做的事"维度，**真的接近无所不能**。
