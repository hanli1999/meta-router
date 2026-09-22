# meta-router — 总入口路由器

> 不做事，只路由：你说"想 X"，它告诉你调哪个 skill / 用哪个工具 / 走哪个组合。

把 Claude 当前会话能调用的所有能力（skill / 工具 / 工作流 / 子agent / memory）做成一张路由表。

---

## 它解决什么问题

你可能装了 N 个 skill（xiuxian / lingbao-analyzer / ...），能调 20+ 工具（WebSearch / Bash / Edit / ...），但每次遇到新问题都要自己"想该用啥"——**meta-router 把这件事自动化**。

- 你说"把芒格做成灵宝" → 它说"用 lingbao-analyzer forge 模式，跑 `forge.py --name 芒格`"
- 你说"每天 9 点提醒我吃药" → 它说"用 CronCreate，cron='57 8 * * *'"
- 你说"审查 100 个文件找 bug" → 它说"用 Workflow pipeline 跑 find → verify → fix"

---

## 安装

```bash
git clone https://github.com/hanli1999/meta-router.git
# 或直接复制到 ~/.claude/skills/meta-router/
```

无需依赖，Python 3.10+ 即可跑路由脚本。

---

## 用法

### 命令行

```bash
# 标准查询（Markdown 输出，含推荐 + 真实命令 + 预期输出）
python3 scripts/route.py --query "把芒格做成灵宝"

# 极简（只输出 skill/工具名）
python3 scripts/route.py --query "X" --format short

# JSON（机器可读）
python3 scripts/route.py --query "X" --format json
```

### 作为 Skill 调用

```
# 触发词
"做 X 该用什么"
"X 用什么 skill"
"总入口"
"meta-router"
"怎么 X"
```

触发后会自动跑 `python3 scripts/route.py --query "..."` 并呈现推荐链路。

---

## 能力矩阵（6 大维度）

| 维度 | 包含 | 适用场景 |
|---|---|---|
| **类比思维** | xiuxian / lingbao-analyzer / Claude 本职 | 任何决策/事件的启发视角 |
| **信息检索** | WebSearch / WebFetch / Grep / Glob | 任何事实查询 |
| **代码生成** | Claude 本职 + Bash + git + gh | 任何编程任务 |
| **文档处理** | Read / Write / Edit / NotebookEdit | 文本/笔记/Jupyter |
| **并行调度** | Agent / Workflow / parallel / pipeline | 多任务并行 |
| **持久化** | memory / Cron / ScheduleWakeup | 跨会话记忆 + 定时 |

完整子能力见 `references/capability-matrix.md`。

---

## 路由规则（20 条）

| # | 规则 | 目标 |
|---|------|------|
| 1 | 类比启发 | xiuxian skill |
| 2 | 灵宝化 | lingbao-analyzer skill |
| 3 | 事实查询 | WebSearch+WebFetch |
| 4 | 写代码 | Claude+Write/Edit |
| 5 | 跑脚本 | Bash |
| 6 | 读文件 | Read |
| 7 | 编辑文件 | Edit |
| 8 | 找文件 | Glob/Grep |
| 9 | GitHub 操作 | Bash+gh CLI |
| 10 | 多 agent 并行 | Workflow+parallel |
| 11 | 长期记忆 | Write+memory |
| 12 | 定时任务 | CronCreate |
| 13 | 跨会话消息 | SendMessage |
| 14 | 大规模审查 | Workflow+pipeline |
| 15 | 学习新领域 | WebSearch+Claude |
| 16 | 投资/创业类比 | xiuxian+lingbao-analyzer |
| 17 | 内容创作 | Claude |
| 18 | 数据分析 | Bash+Python |
| 19 | 自动化工作流 | Cron+Bash+memory |
| 20 | 用户卡住需澄清 | AskUserQuestion |

完整规则见 `references/routing-rules.md`。

---

## 真实边界（诚实声明）

| 边界 | 原因 |
|---|---|
| 物理世界操作 | 无机器人接口 |
| 24/7 持续在线 | 单次会话有上下文限制 |
| 100% 准确 | 幻觉存在，重要决策双重核对 |
| 法律责任 | 签字/合同主体是你 |
| 医疗/法律最终决策权 | 建议可以，决定是你的 |

---

## 测试结果（2026-09-22）

10 个真实 query 全 PASS：

```
✅ 把芒格做成灵宝 → lingbao-analyzer
✅ 按凡人修仙传看 30 岁转行 → xiuxian
✅ 查一下 2026 年 AI 行业最新趋势 → WebSearch+WebFetch
✅ 写一个 Python 脚本批量重命名文件 → Claude+Write/Edit
✅ 跑 python3 hello.py → Bash
✅ 读 SKILL.md 这个文件 → Read
✅ 把 xiuxian skill 开源到 GitHub → Bash+gh CLI
✅ 每天早上 9 点提醒我吃药 → CronCreate
✅ 用多 agent 并行审查代码 → Workflow+parallel
✅ 记住我反对打断型元提示 → Write+memory
```

---

## 引用

- **xiuxian** skill：凡人修仙传类比检索引擎（730 万字）
- **lingbao-analyzer** skill：灵宝类比生成器（12 要素）
- **workflow-authoring** skill：多 agent 工作流编排

---

## License

MIT © 2026 hanli1999