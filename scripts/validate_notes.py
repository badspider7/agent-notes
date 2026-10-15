"""Validate active Agent Notes using the skill's default Markdown format."""

import argparse
from datetime import date
import os
from pathlib import Path
import re


COMMON = ({"问题", "Problem"}, {"考虑过的替代方案", "Alternatives considered"})
REQUIRED = {
    "proposed": ({"提案", "Proposal"}, {"验收条件", "Acceptance criteria"}, {"风险与代价", "Risks"}),
    "implemented": ({"决定", "Decision"}, {"影响与代价", "Consequences"}),
    "rejected": ({"提案", "Proposal"}, {"否决原因", "Rejection reason"}),
}
FORBIDDEN_IMPLEMENTED = {"提案", "Proposal", "计划", "Plan", "迁移计划", "Migration plan", "验收条件", "Acceptance criteria"}


def prose_lines(content):
    """Yield Markdown lines outside fenced code blocks."""
    fence = None
    for line in content.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is None:
            yield line


def validate_note(path, lifecycle):
    """Return default-format violations for one active record."""
    errors = []
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name)
    if not match:
        errors.append("文件名应为 YYYY-MM-DD-lowercase-topic.md")
    else:
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            errors.append("文件名日期无效")
    try:
        lines = list(prose_lines(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError) as error:
        return errors + [f"无法读取 UTF-8 文件：{error}"]
    first = next((line for line in lines if line.strip()), "")
    if not re.fullmatch(r"# \S.*", first):
        errors.append("正文应以非空一级标题开头")
    statuses = [line for line in lines if re.match(r"^Status\s*:", line)]
    if statuses != [f"Status: {lifecycle}"]:
        errors.append(f"应且仅应有一行 Status: {lifecycle}")
    sections = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
        elif line.startswith("# "):
            current = None
        elif current is not None:
            sections[current].append(line)
    for alternatives in COMMON + REQUIRED[lifecycle]:
        present = alternatives.intersection(sections)
        label = " / ".join(sorted(alternatives))
        if not present:
            errors.append(f"缺少二级章节：{label}")
        elif not any(any(line.strip() for line in sections[heading]) for heading in present):
            errors.append(f"章节无正文：{label}")
    if lifecycle == "implemented":
        for heading in sorted(FORBIDDEN_IMPLEMENTED.intersection(sections)):
            errors.append(f"已实施记录不保留计划章节：{heading}")
    return errors


def validate_tree(root):
    """Return violations and record count without reading archives or symlinks."""
    if not root.is_dir():
        return [f"{root}: notes 目录不存在"], 0
    errors = []
    count = 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        dirs[:] = sorted(name for name in dirs if name != "archived" and not (base / name).is_symlink())
        for name in sorted(files):
            path = base / name
            if path.is_symlink() or path.suffix != ".md" or name in {"README.md", "AGENTS.md"}:
                continue
            relative = path.relative_to(root)
            lifecycle = relative.parts[0]
            count += 1
            if lifecycle not in REQUIRED:
                errors.append(f"{relative}: 记录应位于 proposed/、implemented/ 或 rejected/")
                continue
            errors.extend(f"{relative}: {error}" for error in validate_note(path, lifecycle))
    return errors, count


def main():
    """Print actionable validation results and return a process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes_dir", type=Path, help="目标项目的 notes 目录")
    args = parser.parse_args()
    errors, count = validate_tree(args.notes_dir)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"通过：检查了 {count} 篇活动记录；未检查链接、实现依据或归档冻结。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
