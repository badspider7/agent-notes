# Agent Notes

为项目建立和维护 Agent 决策记录的 skill，让维护者和后续 Agent 能查明重要决定的原因、取舍与重新评估条件。

适合记录架构选型、兼容约束、模块职责、安全约束，以及容易反复争论的方案。不用于收集全部生成文档、临时计划或开发流水。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent 加载的入口，定义适用范围和维护流程 |
| [agents/openai.yaml](agents/openai.yaml) | skill 的展示名称、简介和默认提示词 |
| [references/templates.md](references/templates.md) | 项目规则、notes README 和决策记录模板 |
| [scripts/validate_notes.py](scripts/validate_notes.py) | 仅依赖 Python 标准库的默认格式校验器 |
| [scripts/test_validate_notes.py](scripts/test_validate_notes.py) | 校验器的回归测试 |

## 获取与使用

```bash
git clone https://github.com/badspider7/agent-notes.git
```

按所用 Agent 工具的技能加载方式，加载整个 `agent-notes` 目录，保留上述相对目录结构。若工具不支持 skill 加载，也可以让 Agent 阅读 `SKILL.md` 并按其中流程处理目标项目。

明确指定目标项目；skill 所在目录不一定是需要建立决策记录的项目。支持 `$agent-notes` 调用的工具可以使用以下请求：

```text
使用 $agent-notes，为 D:/projects/my-app 初始化决策记录机制。
复用已有项目约定，补充必要的 AGENTS.md 规则和 notes README。
```

```text
使用 $agent-notes，依据当前实现与已确认的讨论，记录任务存储方案的决定。
检查相关旧记录；无法确认的信息标为待确认，不补写不存在的讨论。
```

```text
使用 $agent-notes，审查当前项目的决策记录是否重复或过时。
先报告问题与建议，不修改文件。
```

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

初始化后的查阅和维护由目标项目的 `AGENTS.md` 与 notes README 引导。notes 目录本身不会保证 Agent 自动加载全部记录。

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
