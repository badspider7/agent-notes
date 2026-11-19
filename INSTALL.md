# 给 Agent 的安装说明

本文件供 Codex、Claude Code 或代为配置环境的 Agent 执行。仓库地址：`https://github.com/badspider7/agent-notes.git`。仓库根目录本身就是名为 `agent-notes` 的 skill，不存在额外的 `skills/agent-notes/` 子目录。

## 1. 确定工具和安装范围

遵循用户指定的工具、范围和路径。用户说“给你安装”且当前工具可确定时，安装到当前工具；未指定范围时使用用户级。无法判断工具，或用户要求项目级却无法确定目标项目时，先询问缺失信息。

| 工具 | 用户级（默认） | 项目级 |
| --- | --- | --- |
| Codex | `~/.agents/skills/agent-notes/` | `<项目根>/.agents/skills/agent-notes/` |
| Claude Code | `~/.claude/skills/agent-notes/` | `<项目根>/.claude/skills/agent-notes/` |

`~` 指实际运行 Agent 的用户主目录。WSL 与 Windows 原生环境分别处理。只安装用户要求的工具；用户要求两端都安装时，分别安装并检查。

## 2. 检查已有安装

解析目标绝对路径，检查是否存在同名目录及 `SKILL.md`。也检查当前作用域中是否已有同名 skill，避免无意增加重复安装。

- 不存在：进入安装步骤。
- 已存在且是本仓库的有效安装：报告已安装，不重复克隆；仅在用户要求更新时更新。
- 来源不同、结构不完整或有本地修改：说明冲突，不覆盖、不删除；在需要替换时请用户决定。

更新 Git 安装时，先检查 remote 和工作区状态，确认来源匹配且没有本地修改后使用 `git pull --ff-only`；有冲突或无法快进就停止并报告，不执行 reset、强制覆盖或清理。

## 3. 安装文件

使用 HTTPS 获取仓库，不要求用户配置 SSH Key。可用 Git，也可下载仓库归档；不需要 npm、pip、MCP 或 API Key。

**用户级安装：**创建目标父目录后，将仓库克隆到最终的 `agent-notes` 目录：

```text
git clone https://github.com/badspider7/agent-notes.git <目标绝对路径>
```

使用实际 shell 的参数引用方式处理含空格路径。保留 Git 元数据便于后续按用户要求更新。

**项目级安装：**先将仓库获取到独立的临时目录，再把 `SKILL.md`、`references/`、`scripts/`、`agents/` 复制到最终目录；可一并保留 `README.md` 与 `INSTALL.md`。不要复制 `.git/`，不要在目标项目内创建嵌套 Git 仓库或自动添加 submodule。获取到临时目录的文件应先核对再复制。

安装完成后应至少具有：

```text
agent-notes/
├── SKILL.md
├── agents/openai.yaml
├── references/templates.md
└── scripts/
    ├── validate_notes.py
    └── test_validate_notes.py
```

保持相对路径不变，不要只复制 `SKILL.md`，也不要变成 `agent-notes/agent-notes/SKILL.md`。

## 4. 验证并交付

1. 确认最终目录、以上文件和 `SKILL.md` 的 frontmatter，`name` 应为 `agent-notes`，`description` 应存在。
2. 确认入口中引用的模板与脚本能从安装位置找到。安装本身不需要 Python；有 Python 3.10+ 时，可选运行 `python -m unittest discover -s "<安装目录>/scripts" -p "test_*.py"`。不要为了安装 skill 自动安装 Python 或第三方包。
3. 如果能查看宿主的技能列表，检查是否发现 `agent-notes`。否则明确说明只完成文件检查，提示用户重启会话后确认，不声称已完成宿主调用测试。
4. 报告工具、范围、安装绝对路径、实际验证结果和调用示例：Codex 使用 `$agent-notes`，Claude Code 使用 `/agent-notes`。

用户仅要求安装时到此结束，不修改目标项目的 `AGENTS.md`、`CLAUDE.md` 或 `.agents/notes/`，也不创建示例决策。用户同时要求初始化时，安装完成后再加载最终位置的 `SKILL.md`，对明确的目标项目执行初始化。

安装后示例：

```text
Codex：使用 $agent-notes，为当前项目初始化决策记录机制。
Claude Code：/agent-notes 为当前项目初始化决策记录机制。
```

安装位置参考 [Codex Skills](https://developers.openai.com/codex/skills/) 与 [Claude Code Skills](https://code.claude.com/docs/en/skills)。本说明面向可读写本地 skills 目录的环境；遇到网络、权限或宿主管理策略限制时，报告实际阻碍，不以修改无关设置绕过。
