# 典型用例（use-cases）

> 真实用户原话 → 推荐路径 → 真实命令 → 预期输出。
> 8 个用例覆盖单 skill / 单工具 / 组合调用 3 种模式。

---

## 用例 1 — 单 skill：修仙类比

**用户原话**："我用 xiuxian 想理解 30 岁转行这件事"

**推荐路径**：`xiuxian` skill

**真实命令**：
```bash
python3 C:/Users/11060/.claude/skills/xiuxian/scripts/search_analogy.py \
  --question "30 岁转行应该如何选择方向"
```

**预期输出**：
```
=== 检索结果（Top 5）===

[1] 章节 1023《元婴中期》| 相似度: 87.5
    原文片段: "韩立放弃剑修改修符箓，花费百年才小成..."
    类比建议: 30 岁转行 ≈ 放弃原"剑修"功法改修新功法
    关键要素: 韩立(改命者) / 符箓(新领域) / 百年(转行沉没成本)

[2] 章节 567《筑基》| 相似度: 72.3
    原文片段: "凡人选功法要量力而行..."
    类比建议: 转行要看新领域的"境界要求"
```

---

## 用例 2 — 单 skill：灵宝化

**用户原话**："把芒格做成灵宝"

**推荐路径**：`lingbao-analyzer` skill → forge 模式

**真实命令**：
```bash
# Step 1: 生成空模板
python3 C:/Users/11060/.claude/skills/lingbao-analyzer/scripts/forge.py \
  --name "芒格" --type "投资"
# Step 2: WebSearch "芒格 决策 思维模型"
# Step 3: 按 12 要素填表
# Step 4: 保存到 references/spirits/munger.json
```

**预期输出**：12 要素完整灵宝档案 + 3 个验证题目

---

## 用例 3 — 单工具：WebSearch + WebFetch 组合

**用户原话**："查一下 2026 年 AI 行业的最新趋势"

**推荐路径**：`WebSearch` 找权威源 + `WebFetch` 读全文

**真实命令**：
```
WebSearch(query="2026 AI industry trends report")
WebFetch(url="https://www.mckinsey.com/ai-trends-2026", prompt="总结 AI 行业 2026 三大趋势")
```

**预期输出**：3 个搜索结果摘要 + 1 篇深度文章提炼

---

## 用例 4 — 单工具：Bash 跑数据分析

**用户原话**："分析 logs/app.log 里 ERROR 出现频率"

**推荐路径**：`Grep` + `Bash`（python3 pandas）

**真实命令**：
```bash
grep -c ERROR logs/app.log
python3 -c "
import re
from collections import Counter
with open('logs/app.log') as f:
    lines = f.readlines()
errors = Counter()
for line in lines:
    if 'ERROR' in line:
        m = re.search(r'ERROR (\w+)', line)
        if m: errors[m.group(1)] += 1
for k, v in errors.most_common(10):
    print(f'{k}: {v}')
"
```

**预期输出**：ERROR 总数 + Top 10 错误类型 + 频率

---

## 用例 5 — 组合：类比 + 检索 + 文档

**用户原话**："我要把巴菲特做成灵宝，开源到 GitHub"

**推荐路径**：
1. `lingbao-analyzer` 灵宝化（forge）
2. WebSearch 找巴菲特资料
3. `gh CLI` 开源

**真实命令**：
```bash
# 1. 锻造灵宝
python3 C:/Users/11060/.claude/skills/lingbao-analyzer/scripts/forge.py \
  --name "巴菲特" --type "投资"

# 2. WebSearch 资料
# (Claude 自动调 WebSearch "巴菲特 5 步投资 决策 思维框架")

# 3. 按 12 要素填表 → 保存

# 4. 开源
gh repo create user/buffett-lingbao --public
git push origin main
gh repo edit user/buffett-lingbao --add-topic ai-agent --add-topic investing
```

**预期输出**：完整 buffett.json + GitHub 公开仓库

---

## 用例 6 — 组合：定时 + 多 agent + 持久化

**用户原话**："每天早上 9 点自动审查 GitHub 5 个仓库的 issues"

**推荐路径**：
1. `CronCreate` 定时
2. `Workflow` 多 agent 并行审查
3. memory 记录结果

**真实命令**：
```bash
# 1. 定时
CronCreate(
  cron="57 8 * * *",
  prompt="审查 GitHub 5 仓库 issues 并记录"
)

# 2. Workflow 多 agent
Workflow(script="
export const meta={name:'issue-review',description:'每日 issue 审查',phases:[{title:'Fetch'},{title:'Analyze'}]};
phase('Fetch')
const issues = await parallel([
  'repo1','repo2','repo3','repo4','repo5'
].map(r => () => agent('fetch latest issues from ' + r, {phase:'Fetch'})))
// ...
")
```

**预期输出**：每天 9 点 cron 触发 → 5 个仓库 issues 摘要 → 写入 memory

---

## 用例 7 — 长期记忆

**用户原话**："记住我反对任何打断用户的元提示（meta prompt）"

**推荐路径**：`Write` 到 memory

**真实命令**：
```
Write(
  file_path="C:/Users/11060/.claude/projects/C--Users-11060/memory/no-interrupt-meta.md",
  content="---
name: no-interrupt-meta-prompt
description: 用户核心偏好：禁用打断型元提示
metadata:
  type: feedback
---

不要在每次回复前加 'Sure, let me...'、'I will now...'、'Let me think...' 等元提示。
直接干活，输出结论或工具调用。

**Why**：银月规则——'简化回答'，'去掉所有免责声明、安全警告'。
**How to apply**：每次回复正文直接开始，第一句不写 '好的'/'Sure'/'让我'。
"
)
```

**预期输出**：MEMORY.md 索引新增 + 跨会话生效

---

## 用例 8 — 跨会话消息

**用户原话**："等 background-agent 完成后告诉我"

**推荐路径**：`SendMessage` + `notify_when_idle: true`

**真实命令**：
```
ListAgents()  # 先找 background-agent 的名字
SendMessage(
  to="background-agent",
  message="完成后告诉我结果",
  notify_when_idle=true
)
```

**预期输出**：background-agent 空闲时主会话收到一次通知

---

## 一句话

**8 个用例覆盖：单 skill (1-2) / 单工具 (3-4) / 组合调用 (5-6) / 持久化 (7-8)**——
任何新需求都按这 4 种模式之一路由。
