# 路由规则（routing-rules）

> 用户问什么 → 该调什么。15+ 条规则覆盖常见任务。

## 规则格式

```
规则 #N
- 触发关键词：[关键词列表]
- 推荐路径：[skill 名 / 工具名 / 组合]
- 预期输出：[一句话说明]
- 真实命令：[可执行示例]
```

---

## 规则 #1 — 类比启发
- **触发关键词**：按凡人修仙传看 X、用修仙视角分析 X、修仙类比 X、像不像韩立遇到 X
- **推荐路径**：`xiuxian` skill → `scripts/search_analogy.py --question "X"`
- **预期输出**：原文片段 + 要素名 + 类比建议
- **真实命令**：`python3 C:/Users/11060/.claude/skills/xiuxian/scripts/search_analogy.py --question "30岁转行"`

## 规则 #2 — 灵宝化
- **触发关键词**：灵宝化 X、按灵宝设计 X、做灵宝 X、锻造 X 灵宝
- **推荐路径**：`lingbao-analyzer` skill → `scripts/analyze.py --target "X"` 或 `scripts/forge.py --name "X" --type "..."`
- **预期输出**：12 要素分析 + 三步血祭清单 + 威力评级
- **真实命令**：`python3 C:/Users/11060/.claude/skills/lingbao-analyzer/scripts/forge.py --name "芒格" --type "投资"`

## 规则 #3 — 事实查询
- **触发关键词**：X 是什么、X 怎么样、X 是几号、查 X 资料、搜索 X
- **推荐路径**：`WebSearch`（广）+ `WebFetch`（深）
- **预期输出**：3-5 个搜索结果 + 关键网页全文摘要
- **真实命令**：`WebSearch("巴菲特 5 步投资决策")` → `WebFetch("https://...")` 二次精读

## 规则 #4 — 写代码
- **触发关键词**：写一个 X、用 X 语言实现 Y、写一个脚本、帮我写代码
- **推荐路径**：Claude 本职直接生成（按需调用 `Write` / `Edit`）
- **预期输出**：完整可运行代码（含注释）
- **真实命令**：`Write(file_path="...", content="...")`

## 规则 #5 — 跑脚本/命令
- **触发关键词**：跑 X、执行 X、运行 X 命令、X 出错了
- **推荐路径**：`Bash`（含 `python3` / `git` / `npm` 等）
- **预期输出**：命令返回值（含 stdout / stderr / 退出码）
- **真实命令**：`Bash(command="python3 script.py", description="运行脚本")`

## 规则 #6 — 读文件
- **触发关键词**：读 X 文件、X 文件里有什么、看 X 文件第 N 行
- **推荐路径**：`Read`（含 PDF/图片/Jupyter 支持）
- **预期输出**：文件内容（带行号）
- **真实命令**：`Read(file_path="C:/.../file.py", offset=100, limit=50)`

## 规则 #7 — 编辑文件
- **触发关键词**：改 X 文件的 Y 段、在 X 加 Y、把 X 改成 Y
- **推荐路径**：`Edit`（精确替换）或 `Write`（整体覆盖）
- **预期输出**：diff 行号 + 替换后内容
- **真实命令**：`Edit(file_path="...", old_string="...", new_string="...")`

## 规则 #8 — 找文件
- **触发关键词**：X 文件在哪、找 X 文件、搜索 X 模式
- **推荐路径**：`Glob`（按名）或 `Grep`（按内容）
- **预期输出**：匹配文件路径列表
- **真实命令**：`Glob(pattern="**/*.py")` 或 `Grep(pattern="def main", output_mode="files_with_matches")`

## 规则 #9 — GitHub 操作
- **触发关键词**：推 X 到 GitHub、开源 X、创建 X 仓库、给 X 仓库加 topic
- **推荐路径**：`Bash` + `gh CLI`（先 `unset GITHUB_TOKEN`）
- **预期输出**：仓库 URL + commit hash + 元数据
- **真实命令**：`gh repo create user/X --public --description "..."` → `git push` → `gh repo edit ... --add-topic`

## 规则 #10 — 多 agent 并行
- **触发关键词**：并行做 X、用多 agent X、多线程查 X
- **推荐路径**：`Workflow` + `parallel()`（多维度同时跑）
- **预期输出**：N 个 agent 独立结果 + 汇总
- **真实命令**：`Workflow(script="export const meta={name:'X',description:'X',phases:[{title:'Find'}]};parallel([...])")`

## 规则 #11 — 长期记忆
- **触发关键词**：记住 X、以后 X 都要 X、不要忘 X
- **推荐路径**：`Write` 到 `C:/Users/11060/.claude/projects/C--Users-11060/memory/X.md`
- **预期输出**：MEMORY.md 索引新增一行
- **真实命令**：`Write(file_path="C:/Users/11060/.claude/projects/C--Users-11060/memory/X.md", content="...")`

## 规则 #12 — 定时任务
- **触发关键词**：每天 X 点提醒 Y、每小时检查 X、定时跑 X
- **推荐路径**：`CronCreate`（5 字段 cron）
- **预期输出**：cron job ID + 下次执行时间
- **真实命令**：`CronCreate(cron="57 8 * * *", prompt="提醒 X")`

## 规则 #13 — 跨会话消息
- **触发关键词**：通知 X、告诉 X、X 完成后告诉我、等 X 空闲
- **推荐路径**：`SendMessage` + `notify_when_idle: true`
- **预期输出**：X 收到消息 + 一次空闲通知
- **真实命令**：`SendMessage(to="X", message="...", notify_when_idle=true)`

## 规则 #14 — 大规模审查
- **触发关键词**：审查 X、找出 X 的 bug、全面审计 X、迁移 X
- **推荐路径**：`Workflow` 多阶段流水线（Find → Verify → Fix）
- **预期输出**：已验证的发现列表 + 修复建议
- **真实命令**：`Workflow(script="...pipeline(items, findStage, verifyStage, fixStage)")`

## 规则 #15 — 学习新领域
- **触发关键词**：我想学 X、解释 X、X 怎么入门、X 是什么原理
- **推荐路径**：`WebSearch`（找权威源）+ Claude 本职（讲解）+ 类比（如适用）
- **预期输出**：3-5 个学习资源 + 中学生口吻讲解
- **真实命令**：`WebSearch("X 入门 教程")` → `WebFetch(top_result_url)` → 输出笔记

## 规则 #16 — 投资/创业类比
- **触发关键词**：X 该不该投、如何选 Y、创业做 X 怎么样、X 像不像 Y
- **推荐路径**：`xiuxian` 类比 + `lingbao-analyzer` 灵宝化（如对象是人/思想）
- **预期输出**：修仙映射 + 现代决策框架
- **真实命令**：`/xiuxian` 或"灵宝化 巴菲特"

## 规则 #17 — 内容创作
- **触发关键词**：写一篇 X、写一个 X 故事、写 X 的脚本
- **推荐路径**：Claude 本职（直接生成）
- **预期输出**：完整文章/脚本/故事
- **真实命令**：直接描述需求即可

## 规则 #18 — 数据分析
- **触发关键词**：分析 X 数据、统计 X、X 趋势怎么样、X 的规律
- **推荐路径**：`Bash` + Python（pandas/numpy）+ `Read` 数据文件
- **预期输出**：统计指标 + 图表描述 + 洞察
- **真实命令**：`Bash(command="python3 -c \"import pandas as pd; ...\"")`

## 规则 #19 — 自动化工作流
- **触发关键词**：每天自动 X、自动跑 X、X 完成后自动做 Y
- **推荐路径**：`CronCreate`（定时）+ `Bash`（执行脚本）+ memory（记录）
- **预期输出**：定时任务 ID + 自动化脚本
- **真实命令**：`CronCreate(cron="0 9 * * 1", prompt="跑 weekly_report.py")`

## 规则 #20 — 用户卡住需澄清
- **触发关键词**：用户说"选哪个"、"A 还是 B"、"你想要哪个"
- **推荐路径**：`AskUserQuestion`（1-4 题，支持 preview）
- **预期输出**：用户回答
- **真实命令**：`AskUserQuestion(questions=[{question:"...", options:[...]}])`

---

## 路由优先级（冲突时怎么办）

| 优先级 | 维度 | 原因 |
|---|---|---|
| 1 | 用户明确说的 skill 名 | `/xiuxian` > 关键词推断 |
| 2 | 用户明确说的工具名 | "用 WebSearch" > 默认 |
| 3 | 触发关键词命中 | 按规则表匹配 |
| 4 | 类比启发 | 不确定时优先用 xiuxian 找灵感 |
| 5 | 真实工具执行 | 类比后再用工具落地 |

## 一句话

**先看用户原话有没有明确指向，没有就查路由表，再没有就用 xiuxian 类比启发，最后用真实工具执行**。
