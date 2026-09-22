# GATES.md — meta-router skill（总入口路由器）

## 任务
把 Claude 当前会话内**所有可调用的能力**（skill / 工具 / 工作流 / 子agent / memory）
做成一张"路由表"。用户问"做 X 该用什么" → 立即给出最完整路径。

## Gates（8 项）

### G1 — 能力矩阵文档化
- CHECK: `references/capability-matrix.md` 存在 + 6 大能力全覆盖
- EXPECT:
  - 类比思维（xiuxian / lingbao-analyzer）
  - 信息检索（WebSearch / WebFetch）
  - 代码生成（Claude 本职 + Bash）
  - 文档处理（Read / Write / Edit / NotebookEdit）
  - 并行调度（Agent / Workflow / parallel / pipeline）
  - 持久化（memory / cron / ScheduleWakeup）
- 每类 ≥ 3 个子能力 + 适用场景 + 工具 + 限制

### G2 — 路由规则表
- CHECK: `references/routing-rules.md` 存在 + ≥ 15 条规则
- EXPECT:
  - 每条规则 = 触发关键词 + 推荐路径（skill 名 / 工具名 / 组合）
  - 覆盖：类比 / 检索 / 写代码 / 管文件 / 跑脚本 / 开源 / 长期监控 / 跨会话记忆 / 多任务并行 / 学习新领域 / 决策辅助 / 内容创作 / 数据分析 / 自动化工作流 / 投资类比

### G3 — 典型用例
- CHECK: `references/use-cases.md` 存在 + ≥ 8 个真实用例
- EXPECT:
  - 每个用例 = 用户原话 + 推荐路径 + 预期输出 + 真实命令
  - 覆盖单 skill / 单工具 / 组合调用 3 种模式

### G4 — SKILL.md 11 段齐全
- CHECK: 按 skill-explainer 11 段框架自检
- EXPECT: 11/11 段齐全（标题卡/原则/前置/步骤/工具/降级/检查/边界/小贴士/下一步/案件管家联动）

### G5 — 路由脚本
- CHECK: `scripts/route.py --query "..."` 跑通
- EXPECT: 返回最匹配的 skill 名 / 工具名 + 推荐理由

### G6 — 真实测试
- CHECK: 给 10 个不同类型 query → 路由结果正确
- EXPECT: 10/10 命中正确分类（类比 / 检索 / 代码 / 文件 / 调度 / 持久化 / 组合）

### G7 — 开源准备（LICENSE / README / .gitignore）
- CHECK: 三个文件齐 + 内容合规
- EXPECT:
  - LICENSE = MIT
  - README.md 含简介 + 能力矩阵 + 用法 + 引用
  - .gitignore 标准排除

### G8 — GitHub 推送（可选）
- CHECK: `git ls-remote origin main` 一致
- EXPECT: hanli1999/meta-router 公开仓库 + 8 topics + MIT

## 执行状态（2026-09-22）
- G1: ✅ PASS — capability-matrix.md 6 大能力 × 子能力齐全
- G2: ✅ PASS — routing-rules.md 20 条规则齐全
- G3: ✅ PASS — use-cases.md 8 个真实用例
- G4: ✅ PASS — SKILL.md 11 段齐全 + 案件管家联动块
- G5: ✅ PASS — route.py --query/--format/--short 跑通
- G6: ✅ PASS — 10/10 真实 query 路由全对
- G7: ✅ PASS — LICENSE (MIT) + README + .gitignore
- G8: ⏳ 待跑（等用户决定是否推 GitHub）

## 测试结果详情（G6）

| # | Query | 期望 | 实际 | 状态 |
|---|---|---|---|---|
| 1 | 把芒格做成灵宝 | lingbao-analyzer | lingbao-analyzer | ✅ |
| 2 | 按凡人修仙传看 30 岁转行 | xiuxian | xiuxian | ✅ |
| 3 | 查一下 2026 年 AI 行业最新趋势 | WebSearch+WebFetch | WebSearch+WebFetch | ✅ |
| 4 | 写一个 Python 脚本批量重命名文件 | Claude+Write/Edit | Claude+Write/Edit | ✅ |
| 5 | 跑 python3 hello.py | Bash | Bash | ✅ |
| 6 | 读 SKILL.md 这个文件 | Read | Read | ✅ |
| 7 | 把 xiuxian skill 开源到 GitHub | Bash+gh CLI | Bash+gh CLI | ✅ |
| 8 | 每天早上 9 点提醒我吃药 | CronCreate | CronCreate | ✅ |
| 9 | 用多 agent 并行审查代码 | Workflow+parallel | Workflow+parallel | ✅ |
| 10 | 记住我反对打断型元提示 | Write+memory | Write+memory | ✅ |

**总通过率**: 10/10 = 100%
