# Agent Notes

为项目建立和维护 Agent 决策记录的 skill，让维护者和后续 Agent 能查明重要决定的原因、取舍与重新评估条件。

适合记录架构选型、兼容约束、模块职责、安全约束，以及容易反复争论的方案。不用于收集全部生成文档、临时计划或开发流水。

这是一个标准的目录型 Agent Skill，可安装到 Codex 或 Claude Code。核心是 `SKILL.md`，不需要启动服务、配置 MCP 或申请 API Key。仅在运行可选的格式校验器时需要 Python 3.10+。

例如，项目选择 SQLite 而暂不使用 PostgreSQL：记录当时的部署约束、真实考虑过的替代方案，以及什么条件下应重新评估，让下一个 Agent 能理解原因。

## 快速开始：让 Agent 安装

把下面这段话发给 Codex 或 Claude Code（需要能访问 GitHub 和本地文件）：

```text
请安装 https://github.com/badspider7/agent-notes 这个 skill。
先读取仓库根目录的 INSTALL.md，按其中说明安装到你当前工具的用户级 skills 目录。
保留完整的 skill 文件结构；已有同名目录时先检查，不覆盖本地修改。
本次只安装 skill，不初始化当前项目的决策记录。
完成后告诉我安装路径、验证结果，以及如何调用。
```

给 Agent 的完整操作说明见 [INSTALL.md](INSTALL.md)。安装完成后，再按照下方示例为目标项目初始化。

## 手动安装

下面的用户级安装对本机当前用户的各个项目生效。需要 Git；选择你使用的工具执行对应命令，无需两套都装。

### Codex

macOS / Linux / WSL（Bash）：

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/badspider7/agent-notes.git "$HOME/.agents/skills/agent-notes"
```

Windows（PowerShell）：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.agents/skills" | Out-Null
git clone https://github.com/badspider7/agent-notes.git "$HOME/.agents/skills/agent-notes"
```

### Claude Code

macOS / Linux / WSL（Bash）：

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/badspider7/agent-notes.git "$HOME/.claude/skills/agent-notes"
```

Windows（PowerShell）：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.claude/skills" | Out-Null
git clone https://github.com/badspider7/agent-notes.git "$HOME/.claude/skills/agent-notes"
```

若目标目录已经存在，不要直接覆盖或删除，按 [INSTALL.md](INSTALL.md) 检查是否已安装。Windows 原生工具和 WSL 的用户目录不同，安装到实际运行 Agent 的环境中。

### 只对一个项目启用

把本仓库的 skill 文件复制到下面的项目目录，保持相对结构，团队可将其提交到版本控制。不要把本仓库的 `.git/` 复制进去。

| 工具 | 用户级目录 | 项目级目录（相对于项目根） | 显式调用 |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/agent-notes/` | `.agents/skills/agent-notes/` | `$agent-notes` |
| Claude Code | `~/.claude/skills/agent-notes/` | `.claude/skills/agent-notes/` | `/agent-notes` |

目标布局必须是 `<skills目录>/agent-notes/SKILL.md`，不能多嵌套一层 `agent-notes/`。至少保留 `SKILL.md`、`references/`、`scripts/` 和 `agents/`；不要只复制入口文件。`agents/openai.yaml` 是 Codex 的可选展示元数据，Claude Code 使用 `SKILL.md` 即可。

路径和调用方式依据 [Codex 官方 Skills 文档](https://developers.openai.com/codex/skills/)及 [Claude Code 官方 Skills 文档](https://code.claude.com/docs/en/skills)。这里的手动步骤面向可读取本地 skills 目录的环境；云端会话需要在其运行环境另行配置。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent 加载的入口，定义适用范围和维护流程 |
| [INSTALL.md](INSTALL.md) | 给 Agent 的安装步骤、检查方法及安装边界 |
| [agents/openai.yaml](agents/openai.yaml) | skill 的展示名称、简介和默认提示词 |
| [references/templates.md](references/templates.md) | 项目规则、notes README 和决策记录模板 |
| [scripts/validate_notes.py](scripts/validate_notes.py) | 仅依赖 Python 标准库的默认格式校验器 |
| [scripts/test_validate_notes.py](scripts/test_validate_notes.py) | 校验器的回归测试 |

## 安装后如何使用

在**目标项目**中打开 Agent 会话。Codex CLI / IDE 可用 `/skills` 查看或输入 `$agent-notes` 选择；Claude Code 输入 `/agent-notes` 调用。若未发现 skill，先检查安装位置和目录层级，再重启会话。

第一次使用，先初始化项目。Codex 示例：

```text
使用 $agent-notes，为当前项目初始化决策记录机制。
复用已有项目约定，补充必要的项目规则入口和 notes README，不生成虚构记录。
```

Claude Code 示例：

```text
/agent-notes 为当前项目初始化决策记录机制。
复用已有项目约定，补充必要的项目规则入口和 notes README，不生成虚构记录。
```

也可把“当前项目”换成明确路径，例如 `D:/projects/my-app`。skill 的安装目录与保存决策的目标项目是两个位置。

后续记录或审查决策：

```text
使用 $agent-notes，依据当前实现与已确认的讨论，记录任务存储方案的决定。
检查相关旧记录；无法确认的信息标为待确认，不补写不存在的讨论。
```

```text
使用 $agent-notes，审查当前项目的决策记录是否重复或过时。
先报告问题与建议，不修改文件。
```

在 Claude Code 中将示例开头的“使用 $agent-notes，”换成 `/agent-notes `。两者也可根据任务描述自动选择 skill；需要明确使用时，优先显式调用。

初始化后，项目规则会引导日常开发时查找和更新相关记录，无需每次调用 skill。规则指引依赖 Agent 读取和执行，不是自动运行的后台程序，也不会把所有历史记录一次性加载。

## 目标项目中的记录

默认位置如下；项目已有 ADR 或其他决策体系时优先复用。

```text
my-app/
├── AGENTS.md
└── .agents/notes/
    ├── README.md
    ├── proposed/       # 尚未完成的提案
    ├── implemented/    # 有实现证据的决定
    └── rejected/       # 已明确否决且理由仍有价值的方案
```

初始化时不生成虚构记录，生命周期目录在出现记录时才创建。文件名使用 `YYYY-MM-DD-topic.md`，日期表示首次提出时间。模板和各状态的必要章节见 [templates.md](references/templates.md)。

- 同一决定的事实变化更新原记录；改变决定及其理由时新建记录，并说明替代范围、互相链接。
- 提案只有在实现证据支持后才转为已实施；未获回复不代表否决。
- 新增记录时审查相关旧记录，保留仍有效的约束和独有理由。
- 归档、合并和删除遵循项目政策及用户授权；不按年龄或数量自动清理。

初始化后的查阅和维护由目标项目的规则文件与 notes README 引导。Codex 使用 `AGENTS.md`；Claude Code 复用可加载的 `AGENTS.md` 或使用 `CLAUDE.md`，两端共用时可在根 `CLAUDE.md` 中用 `@AGENTS.md` 导入规则，避免重复维护正文。具体加载行为见 [Claude Code 项目记忆文档](https://code.claude.com/docs/en/memory)。notes 目录本身不会保证 Agent 自动加载全部记录。

## 格式校验

校验器使用 Python 3.10 或更新版本，无需安装第三方依赖。在本仓库根目录执行，并将路径换成实际目标项目：

```bash
python scripts/validate_notes.py "D:/projects/my-app/.agents/notes"
```

校验器检查活动记录的命名、真实日期、唯一状态行、状态与目录的一致性，以及必要章节是否有正文；支持中文或英文章节和状态目录下的分类子目录。忽略 `archived/`、符号链接、`README.md` 和 `AGENTS.md`。

通过时返回退出码 `0`，格式错误或目录不存在时返回 `1`。空目录会报告检查了 `0` 篇记录，不代表初始化已完成。

它不检查相对链接、实现真实性或归档冻结，也不验证项目自定义格式。使用自定义约定时优先运行项目自己的检查。

## 开发验证

在仓库根目录运行现有回归测试：

```bash
python -m unittest discover -s scripts -p "test_*.py" -v
```

修改记录格式时，同步维护 `SKILL.md`、模板和校验器，并核对 README 中的使用说明。只改文档时仍应检查相对链接；脚本通过不能代替对决策内容的核对。
