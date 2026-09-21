#!/usr/bin/env python3
"""Create non-overwriting continuity files for an AI-assisted project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def safe_title(value: str) -> str:
    value = re.sub(r"[\r\n]+", " ", value).strip()
    return value or "Project"


def readme_text(project: str, language: str) -> str:
    if language == "zh":
        return f"""# {project}

## 项目目标

说明项目为什么存在、要解决什么问题，以及当前最重要的成功标准。

## 当前状态

- 状态：探索 / 开发 / 验证 / 生产
- 最近可用版本：
- 已知限制：
- 下一步：

## 快速开始

```text
填写安装、运行、测试或使用步骤。
```

## 目录说明

| 路径 | 用途 |
|---|---|
| `src/` | 可执行代码和测试 |
| `data/` | 数据及数据说明；敏感数据不得直接进入公开仓库 |
| `docs/` | 需求、架构、操作手册和 SOP |
| `papers/` | 论文、标准、报告和阅读笔记 |
| `results/` | 实验结果、图表和交付物 |
| `AI_History/` | 决策、问题闭环和被否决方案 |

只保留真实存在的目录，不要为了结构完整创建空目录。

## 架构与关键决策

链接到 `docs/` 和 `AI_History/` 中的权威说明，不在这里复制大段内容。

## 数据与安全边界

- 哪些数据属于公开、内部、机密、受限；
- 哪些文件可以进入 Git；
- 哪些资产需要外部备份或加密存储；
- 哪些操作必须人工批准。

## 测试与验证

说明运行测试、验收结果和恢复项目的具体方法。

## 维护规则

重要修改后同步更新 README、AGENTS.md 和必要的 AI_History 决策记录。
"""
    return f"""# {project}

## Purpose

Explain why the project exists, which problem it solves, and the most important success criteria.

## Current State

- Status: exploration / development / validation / production
- Last known-good version:
- Known limitations:
- Next step:

## Quick Start

```text
Add installation, run, test, or usage steps here.
```

## Structure

| Path | Purpose |
|---|---|
| `src/` | Executable code and tests |
| `data/` | Data plus schemas/manifests; sensitive data must not enter a public repository |
| `docs/` | Specifications, architecture, operations, and SOPs |
| `papers/` | Papers, standards, reports, and reading notes |
| `results/` | Experiment output, figures, and deliverables |
| `AI_History/` | Decisions, problem resolutions, and rejected approaches |

Keep only paths that have a real role. Do not create empty directories for appearance.

## Architecture And Decisions

Link to authoritative documents in `docs/` or `AI_History/` instead of copying large explanations here.

## Data And Safety Boundaries

- Which data is public, internal, confidential, or restricted;
- Which files may enter Git;
- Which assets need external or encrypted backup;
- Which actions require human approval.

## Testing And Verification

Describe how to run tests, review results, and restore the project.

## Maintenance

After significant changes, update this README, `AGENTS.md`, and any relevant `AI_History/` decision record.
"""


def agents_text(project: str, language: str) -> str:
    if language == "zh":
        return f"""# Agent 工作约定：{project}

本文件是项目的权威 Agent 指引。若存在 `CLAUDE.md`，它只负责指向本文件，不复制另一套规则。

## 任务开始前

1. 阅读 `README.md`、本文件和相关 `docs/`、`AI_History/` 记录。
2. 检查 Git 状态和现有改动，不覆盖用户未提交的工作。
3. 先确认数据边界；客户数据、合同、报价、密钥和内部路径默认视为敏感。

## 允许与禁止

- 优先做最小、可验证的改动。
- 不擅自重构无关代码、改变公共接口或删除逻辑。
- 不自动提交、推送、发布或发送外部消息，除非用户明确要求。
- 不把敏感数据上传到公共模型、公共仓库或未批准的外部服务。

## 修改流程

1. 找到权威文件和现有实现，不依赖聊天记忆。
2. 修改前确认当前可运行基线；必要时先建立 Git checkpoint。
3. 小步修改，保留原有行为，运行相关测试或验证。
4. 重要修复或设计选择写入 `AI_History/`。
5. 任务结束时报告改动文件、验证结果和未解决问题。

## 数据与文件

- 在 `.gitignore` 中排除密钥、本地 Agent 状态和生成物。
- 大文件、客户原始数据、模型和视频默认使用外部存储与备份，不直接塞入 Git。
- 需要提交结构化数据时，先确认来源、授权、敏感级别和可复现说明。

## 测试要求

在这里填写项目特有测试命令、回归样例、验收标准和不能破坏的行为。

## 领域约束

在这里填写业务规则、计算口径、接口兼容性、法规或出口管制等约束。

## 完成标准

- 改动范围清晰；
- 测试或验证证据充分；
- 文档和决策记录已更新；
- 未引入未披露的敏感数据或依赖。
"""
    return f"""# Agent Instructions: {project}

This file is the canonical agent instruction source. If `CLAUDE.md` exists, it must only point here rather than duplicate a second ruleset.

## Before Starting

1. Read `README.md`, this file, and relevant files under `docs/` and `AI_History/`.
2. Inspect Git state and existing user changes. Never overwrite uncommitted work.
3. Establish the data boundary first. Customer data, contracts, pricing, credentials, and internal paths are sensitive by default.

## Allowed And Forbidden

- Prefer the smallest verifiable change.
- Do not refactor unrelated code, change public interfaces, or delete logic without explicit justification.
- Do not commit, push, publish, or send external messages unless the user explicitly requests it.
- Do not upload sensitive data to public models, public repositories, or unapproved services.

## Change Workflow

1. Find the authoritative file and current implementation; do not rely on chat memory.
2. Confirm a working baseline and create a Git checkpoint when appropriate.
3. Make a small change and run the relevant tests or validation.
4. Record significant fixes or design choices under `AI_History/`.
5. At completion, report changed files, verification evidence, and unresolved issues.

## Data And Files

- Use `.gitignore` to exclude secrets, local agent state, and generated artifacts.
- Keep large files, customer raw data, models, and videos in approved external storage by default.
- Before committing structured data, confirm provenance, authorization, sensitivity, and reproducibility notes.

## Testing Requirements

Add project-specific test commands, regression cases, acceptance criteria, and behavior that must not break.

## Domain Constraints

Add business rules, calculation definitions, interface compatibility, legal constraints, or export-control requirements here.

## Definition Of Done

- The change scope is coherent.
- Test or verification evidence exists.
- Documentation and decision records are current.
- No undisclosed sensitive data or dependency was introduced.
"""


def claude_text(language: str) -> str:
    if language == "zh":
        return """# Claude Code 指引

项目 Agent 规则以 `AGENTS.md` 为唯一权威来源。

请先阅读并遵守根目录 `AGENTS.md`、`README.md` 以及相关 `docs/`、`AI_History/` 文件。不要在本文件复制第二套规则，以免规则漂移。
"""
    return """# Claude Code Instructions

The project's agent rules are canonical in `AGENTS.md`.

Read and follow the root `AGENTS.md`, `README.md`, and relevant files in `docs/` and `AI_History/`. Do not duplicate a second ruleset here; duplicated rules drift over time.
"""


def gitignore_text() -> str:
    return """# Secrets and local credentials
.env
.env.*
!.env.example
*.key
*.pem
*.p12
*.pfx
credentials.json
secrets.json
secrets.yaml
secrets.yml
id_rsa
id_ed25519
kubeconfig
.npmrc
.pypirc

# Local agent/session state
.claude/
.codex/
.cursor/
.continue/
.aider*

# Operating system and editor state
.DS_Store
Thumbs.db
*.swp
*.swo
.idea/
.vscode/*.local.json

# Python and test caches
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# JavaScript build output
node_modules/
dist/
build/
.next/
coverage/

# Generated/local artifacts: review before enabling project-wide patterns
# data/raw/
# results/generated/
# *.log
# *.tmp
"""


def history_readme_text(language: str) -> str:
    if language == "zh":
        return """# AI 决策与问题记录

本目录保存经过压缩、可长期复用的决策记录，不保存完整聊天记录。

一次两小时调试不需要复制 300 条消息，只需要留下：

```markdown
# 简短标题

- 日期：YYYY-MM-DD
- 状态：proposed | accepted | rejected | superseded
- 相关文件：

## 背景

为什么必须处理这个问题。

## 问题

发生了什么，或需要作出什么选择。

## 方案比较

列出真正考虑过的方案。

## 决策

选择了什么，为什么。

## 后果与风险

得到什么，牺牲什么，还剩下什么风险。

## 验证

哪个测试、证据或评审支持这个决定。

## 被否决方案

哪些方案看起来可行但被否决，原因是什么。

## 后续事项

哪些问题仍未解决。
```

文件名使用日期前缀，例如 `2026-09-14-singular-matrix.md`。原始 Session 只用于恢复工作现场。
"""
    return """# AI Decision And Problem Records

This directory stores compressed, durable decisions. It is not a copy of the full chat history.

A two-hour debugging session does not need 300 messages preserved. It needs a record such as:

```markdown
# Short Title

- Date: YYYY-MM-DD
- Status: proposed | accepted | rejected | superseded
- Related files:

## Context

Why this needed attention.

## Problem

What happened, or which choice was required.

## Options Considered

List the approaches actually considered.

## Decision

What was chosen and why.

## Consequences And Risks

What improves, what becomes harder, and what risk remains.

## Verification

Which test, evidence, or review supports the decision.

## Rejected Approaches

Which plausible approaches were rejected, and why.

## Follow-up

What remains unresolved.
```

Use a date prefix for filenames, for example `2026-09-14-singular-matrix.md`. Keep raw sessions separate; use them to recover a work scene, not as the knowledge base.
"""


def docs_readme_text(language: str) -> str:
    if language == "zh":
        return """# 文档索引

在这里链接项目的需求、架构、接口、操作手册、SOP、测试和运维文档。

不要让关键知识只存在于聊天记录或某次 Agent Session 中。
"""
    return """# Documentation Index

Link the project's specifications, architecture, interfaces, operations, SOPs, tests, and maintenance guides here.

Do not leave critical knowledge only in chat history or an agent session.
"""


def planned_files(project: str, language: str) -> dict[Path, str]:
    return {
        Path("README.md"): readme_text(project, language),
        Path("AGENTS.md"): agents_text(project, language),
        Path("CLAUDE.md"): claude_text(language),
        Path(".gitignore"): gitignore_text(),
        Path("AI_History/README.md"): history_readme_text(language),
        Path("docs/README.md"): docs_readme_text(language),
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Workspace root")
    parser.add_argument(
        "--project-name",
        default=None,
        help="Project title used in generated files (default: directory name)",
    )
    parser.add_argument(
        "--language",
        choices=("en", "zh"),
        default="en",
        help="Template language (default: en)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Create missing files. Without this flag, perform a dry run only.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"Workspace does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"Workspace is not a directory: {root}", file=sys.stderr)
        return 2

    project = safe_title(args.project_name or root.name)
    results: list[dict[str, Any]] = []
    for relative, content in planned_files(project, args.language).items():
        target = root / relative
        if target.exists():
            results.append({"path": str(target), "action": "skip_existing"})
            continue
        if args.write:
            write_text(target, content)
            results.append({"path": str(target), "action": "created"})
        else:
            results.append({"path": str(target), "action": "would_create"})

    if args.json:
        print(json.dumps({"workspace": str(root), "files": results}, ensure_ascii=True, indent=2))
    else:
        mode = "WRITE" if args.write else "DRY RUN"
        print(f"Workspace: {root}")
        print(f"Mode: {mode}")
        for item in results:
            print(f"  {item['action']:<13} {item['path']}")
        if not args.write:
            print("No files were changed. Re-run with --write after reviewing the plan.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())