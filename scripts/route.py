#!/usr/bin/env python3
"""route.py — meta-router 路由脚本

输入: --query "用户原话"
处理:
    1. 关键词匹配（20 条路由规则）
    2. 优先级排序（skill > 工具 > 组合）
    3. 返回最匹配的路径 + 真实命令 + 预期输出
输出: 推荐链路（markdown / json / short）

用法:
    python3 route.py --query "把芒格做成灵宝"
    python3 route.py --query "查 2026 AI 趋势"
    python3 route.py --query "X" --format json
    python3 route.py --query "X" --format short
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


BASE_DIR = Path(__file__).parent.parent
RULES_PATH = BASE_DIR / "references" / "routing-rules.md"


# 路由规则表（程序化版，与 routing-rules.md 同步）
ROUTING_RULES = [
    {
        "id": 1,
        "name": "类比启发（xiuxian）",
        "keywords": ["凡人修仙传", "修仙", "韩立", "墨大夫", "南宫婉", "秘境", "类比"],
        "priority": 9,
        "path_type": "skill",
        "target": "xiuxian",
        "command": 'python3 C:/Users/11060/.claude/skills/xiuxian/scripts/search_analogy.py --question "{q}"',
        "expected_output": "原文片段 + 要素名 + 类比建议（Top 5）"
    },
    {
        "id": 2,
        "name": "灵宝化（lingbao-analyzer）",
        "keywords": ["灵宝化", "做灵宝", "做成灵宝", "按灵宝", "灵宝分析", "锻造灵宝", "通天灵宝", "灵宝"],
        "priority": 10,
        "path_type": "skill",
        "target": "lingbao-analyzer",
        "command": 'python3 C:/Users/11060/.claude/skills/lingbao-analyzer/scripts/forge.py --name "{q_extract}" --type "通用"',
        "expected_output": "12 要素灵宝档案 + 三步血祭清单 + 威力评级"
    },
    {
        "id": 3,
        "name": "事实查询",
        "keywords": ["是什么", "怎么样", "是几号", "查", "搜索", "资料", "新闻", "趋势"],
        "priority": 7,
        "path_type": "tool",
        "target": "WebSearch+WebFetch",
        "command": 'WebSearch(query="{q}") → WebFetch(top_url, prompt="总结关键信息")',
        "expected_output": "3-5 个搜索结果 + 关键网页全文摘要"
    },
    {
        "id": 4,
        "name": "写代码",
        "keywords": ["python", "javascript", "java", "写一个", "写代码", "写脚本", "帮我写", "实现一个", "代码", "脚本", "函数", "类", "模块", "编程"],
        "priority": 8,
        "path_type": "tool",
        "target": "Claude+Write/Edit",
        "command": 'Claude 本职生成 → Write(file_path, content) 或 Edit(file_path, old, new)',
        "expected_output": "完整可运行代码（含注释）"
    },
    {
        "id": 5,
        "name": "跑脚本/命令",
        "keywords": ["跑", "执行", "运行", "命令", "出错了", "报错", "python3", "shell", "命令行", "终端", "shell命令"],
        "priority": 9,
        "path_type": "tool",
        "target": "Bash",
        "command": 'Bash(command="{q_extract}", description="执行命令")',
        "expected_output": "命令返回值（stdout / stderr / 退出码）"
    },
    {
        "id": 6,
        "name": "读文件",
        "keywords": ["读", "打开", "看看", "显示", "内容是什么"],
        "priority": 7,
        "path_type": "tool",
        "target": "Read",
        "command": 'Read(file_path="{q_extract}")',
        "expected_output": "文件内容（带行号）"
    },
    {
        "id": 7,
        "name": "编辑文件",
        "keywords": ["改", "替换", "修改", "加一行", "删除", "调整"],
        "priority": 7,
        "path_type": "tool",
        "target": "Edit",
        "command": 'Edit(file_path, old_string, new_string)',
        "expected_output": "diff 行号 + 替换后内容"
    },
    {
        "id": 8,
        "name": "找文件",
        "keywords": ["在哪", "找文件", "搜索文件", "哪个目录"],
        "priority": 7,
        "path_type": "tool",
        "target": "Glob/Grep",
        "command": 'Glob(pattern="**/X") 或 Grep(pattern="...", output_mode="files_with_matches")',
        "expected_output": "匹配文件路径列表"
    },
    {
        "id": 9,
        "name": "GitHub 操作",
        "keywords": ["github", "git push", "开源", "仓库", "repo", "创建仓库", "add topic"],
        "priority": 8,
        "path_type": "combo",
        "target": "Bash+gh CLI",
        "command": 'unset GITHUB_TOKEN && gh repo create user/X --public --description "..." && git push && gh repo edit ... --add-topic',
        "expected_output": "仓库 URL + commit hash + 元数据"
    },
    {
        "id": 10,
        "name": "多 agent 并行",
        "keywords": ["并行", "多agent", "多agent", "分头做", "多线程", "并行审查", "并行做"],
        "priority": 7,
        "path_type": "combo",
        "target": "Workflow+parallel",
        "command": 'Workflow(script="...parallel([...])")',
        "expected_output": "N 个 agent 独立结果 + 汇总"
    },
    {
        "id": 11,
        "name": "长期记忆",
        "keywords": ["记住", "以后都要", "不要忘", "跨会话", "记忆"],
        "priority": 7,
        "path_type": "tool",
        "target": "Write+memory",
        "command": 'Write(file_path="C:/Users/11060/.claude/projects/C--Users-11060/memory/{slug}.md", content="...")',
        "expected_output": "MEMORY.md 索引新增一行 + 跨会话生效"
    },
    {
        "id": 12,
        "name": "定时任务",
        "keywords": ["每天", "每小时", "定时", "提醒", "自动跑"],
        "priority": 7,
        "path_type": "tool",
        "target": "CronCreate",
        "command": 'CronCreate(cron="M H DoM Mon DoW", prompt="{q_extract}")',
        "expected_output": "cron job ID + 下次执行时间"
    },
    {
        "id": 13,
        "name": "跨会话消息",
        "keywords": ["通知", "告诉", "完成后", "等空闲"],
        "priority": 6,
        "path_type": "tool",
        "target": "SendMessage",
        "command": 'ListAgents() → SendMessage(to=X, message=Y, notify_when_idle=true)',
        "expected_output": "X 收到消息 + 一次空闲通知"
    },
    {
        "id": 14,
        "name": "大规模审查",
        "keywords": ["审查", "审计", "找bug", "迁移", "全面"],
        "priority": 6,
        "path_type": "combo",
        "target": "Workflow+pipeline",
        "command": 'Workflow(script="...pipeline(items, findStage, verifyStage, fixStage)")',
        "expected_output": "已验证的发现列表 + 修复建议"
    },
    {
        "id": 15,
        "name": "学习新领域",
        "keywords": ["学习", "入门", "解释", "原理", "教程", "怎么学"],
        "priority": 7,
        "path_type": "combo",
        "target": "WebSearch+Claude",
        "command": 'WebSearch("X 入门 教程") → WebFetch(top_url) → 输出笔记',
        "expected_output": "3-5 个学习资源 + 中学生口吻讲解"
    },
    {
        "id": 16,
        "name": "投资/创业类比",
        "keywords": ["该不该投", "如何选", "创业", "像不像", "风险"],
        "priority": 7,
        "path_type": "combo",
        "target": "xiuxian+lingbao-analyzer",
        "command": '/xiuxian 或 "灵宝化 X"',
        "expected_output": "修仙映射 + 现代决策框架"
    },
    {
        "id": 17,
        "name": "内容创作",
        "keywords": ["写一篇", "写个故事", "文案", "作文", "小说", "诗歌", "散文", "剧本"],
        "priority": 7,
        "path_type": "tool",
        "target": "Claude",
        "command": '直接描述需求即可',
        "expected_output": "完整文章/文案/故事"
    },
    {
        "id": 18,
        "name": "数据分析",
        "keywords": ["分析数据", "统计", "趋势", "规律", "频率", "平均值"],
        "priority": 7,
        "path_type": "combo",
        "target": "Bash+Python",
        "command": 'Bash(command="python3 -c \\"import pandas as pd; ...\\"")',
        "expected_output": "统计指标 + 图表描述 + 洞察"
    },
    {
        "id": 19,
        "name": "自动化工作流",
        "keywords": ["每天自动", "自动跑", "完成后自动", "工作流", "流程"],
        "priority": 7,
        "path_type": "combo",
        "target": "Cron+Bash+memory",
        "command": 'CronCreate(cron, prompt="跑 X") + Bash(execute) + Write(memory record)',
        "expected_output": "定时任务 ID + 自动化脚本"
    },
    {
        "id": 20,
        "name": "用户卡住需澄清",
        "keywords": ["选哪个", "A还是B", "你想要哪个"],
        "priority": 5,
        "path_type": "tool",
        "target": "AskUserQuestion",
        "command": 'AskUserQuestion(questions=[{question, options}])',
        "expected_output": "用户回答"
    },
]


def score_rule(rule: dict, query: str) -> int:
    """对单条规则打分（关键词命中数 × 优先级）"""
    hits = sum(1 for kw in rule["keywords"] if kw in query)
    return hits * rule["priority"]


def extract_keyword(query: str, rules: list) -> str:
    """从 query 里提取关键参数（如灵宝化 X → X）"""
    patterns = [
        r"灵宝化\s*(\S+)",
        r"做灵宝\s*(\S+)",
        r"按灵宝.*?(\S+)",
        r"读\s*(\S+)",
        r"跑\s*(\S+)",
        r"执行\s*(\S+)",
    ]
    for p in patterns:
        m = re.search(p, query)
        if m:
            return m.group(1)
    return query


def route(query: str, format: str = "markdown") -> dict:
    """核心路由函数"""
    scored = [(score_rule(r, query), r) for r in ROUTING_RULES]
    scored.sort(key=lambda x: x[0], reverse=True)

    top_score, top_rule = scored[0] if scored else (0, None)
    second_score, second_rule = scored[1] if len(scored) > 1 else (0, None)

    # 如果都没命中，用 xiuxian 兜底
    if top_score == 0:
        top_rule = ROUTING_RULES[0]  # xiuxian
        top_rule = dict(top_rule, name="兜底：xiuxian 类比启发")
        top_score = 1

    extracted = extract_keyword(query, ROUTING_RULES)

    return {
        "query": query,
        "primary": {
            "rule_id": top_rule["id"],
            "name": top_rule["name"],
            "score": top_score,
            "path_type": top_rule["path_type"],
            "target": top_rule["target"],
            "command": top_rule["command"].replace("{q}", query).replace("{q_extract}", extracted),
            "expected_output": top_rule["expected_output"]
        },
        "secondary": {
            "rule_id": second_rule["id"] if second_rule else None,
            "name": second_rule["name"] if second_rule else None,
            "score": second_score,
            "target": second_rule["target"] if second_rule else None
        } if second_rule else None,
        "all_ranked": [
            {"rule_id": r["id"], "name": r["name"], "score": s}
            for s, r in scored[:5] if s > 0
        ]
    }


def format_markdown(result: dict) -> str:
    """Markdown 输出"""
    p = result["primary"]
    s = result["secondary"]
    md = f"""# 路由结果

## 用户原话
`{result['query']}`

## 主推荐（命中 #{p['rule_id']} · {p['name']} · 得分 {p['score']}）

- **路径类型**：{p['path_type']}
- **目标**：{p['target']}
- **真实命令**：
  ```
  {p['command']}
  ```
- **预期输出**：{p['expected_output']}
"""
    if s:
        md += f"""
## 备选（命中 #{s['rule_id']} · {s['name']} · 得分 {s['score']}）

- **目标**：{s['target']}

"""
    md += "## Top 5 候选\n\n"
    md += "| # | 规则 | 得分 |\n|---|------|------|\n"
    for r in result["all_ranked"]:
        md += f"| {r['rule_id']} | {r['name']} | {r['score']} |\n"

    return md


def format_short(result: dict) -> str:
    """极简输出"""
    p = result["primary"]
    return f"{p['target']}"


def main():
    parser = argparse.ArgumentParser(description="meta-router 路由脚本")
    parser.add_argument("--query", "-q", required=True, help="用户原话")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "short"],
                        default="markdown", help="输出格式")
    args = parser.parse_args()

    result = route(args.query, args.format)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "short":
        print(format_short(result))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
