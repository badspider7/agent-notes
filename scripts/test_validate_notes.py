"""Exercise valid records, invalid records, and archive exclusion."""

from pathlib import Path
import tempfile
import unittest

from validate_notes import validate_tree


class ValidateNotesTests(unittest.TestCase):
    """Check observable validation outcomes in isolated temporary directories."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        templates = (Path(__file__).parents[1] / "references" / "templates.md").read_text(encoding="utf-8")
        self.proposed = templates.split("## 提案模板\n", 1)[1].split("```markdown\n", 1)[1].split("```", 1)[0]
        self.implemented = templates.split("## 已实施模板\n", 1)[1].split("```markdown\n", 1)[1].split("```", 1)[0]

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_templates_and_nested_classification(self):
        self.write("proposed/2026-10-15-storage.md", self.proposed)
        self.write("implemented/architecture/2026-10-15-plugin.md", self.implemented)
        rejected = self.proposed.replace("Status: proposed", "Status: rejected") + "\n## 否决原因\n\n约束不满足。\n"
        self.write("rejected/2026-10-15-cache.md", rejected)
        self.assertEqual(validate_tree(self.root), ([], 3))

    def test_invalid_filename_and_calendar_date(self):
        for name in ("topic.md", "2026-02-30-topic.md"):
            with self.subTest(name=name):
                self.write(f"proposed/{name}", self.proposed)
                errors, _ = validate_tree(self.root)
                self.assertTrue(any(name in error for error in errors))

    def test_status_mismatch_and_duplicate(self):
        for status in ("Status: implemented", "Status: proposed\nStatus: proposed"):
            with self.subTest(status=status):
                self.write("proposed/2026-10-15-topic.md", self.proposed.replace("Status: proposed", status))
                self.assertTrue(any("Status:" in error for error in validate_tree(self.root)[0]))

    def test_missing_and_empty_required_sections(self):
        for section in ("## 无关章节\n\n事实。", "## 考虑过的替代方案\n\n"):
            with self.subTest(section=section):
                prefix, rest = self.proposed.split("## 考虑过的替代方案", 1)
                suffix = "## 验收条件" + rest.split("## 验收条件", 1)[1]
                self.write("proposed/2026-10-15-topic.md", prefix + section + "\n" + suffix)
                self.assertTrue(any("章节" in error for error in validate_tree(self.root)[0]))

    def test_fenced_examples_cannot_supply_status_or_sections(self):
        self.write("proposed/2026-10-15-topic.md", "# 示例\n\n```markdown\n" + self.proposed + "```\n")
        errors, _ = validate_tree(self.root)
        self.assertTrue(any("Status:" in error for error in errors))
        self.assertTrue(any("缺少二级章节" in error for error in errors))

    def test_implemented_rejects_proposal_sections(self):
        self.write("implemented/2026-10-15-topic.md", self.implemented + "\n## 验收条件\n\n尚待完成。\n")
        self.assertTrue(any("不保留计划章节" in error for error in validate_tree(self.root)[0]))

    def test_archives_and_supporting_files_are_excluded(self):
        self.write("archived/topic.md", "historical format")
        self.write("README.md", "project rules")
        self.write("implemented/AGENTS.md", "local rules")
        self.assertEqual(validate_tree(self.root), ([], 0))

    def test_wrong_lifecycle_and_missing_root_fail(self):
        self.write("other/2026-10-15-topic.md", self.proposed)
        self.assertTrue(validate_tree(self.root)[0])
        self.assertTrue(validate_tree(self.root / "missing")[0])

    def test_english_headings_are_accepted(self):
        content = "# Storage\n\nStatus: implemented\n"
        for heading in ("Problem", "Decision", "Alternatives considered", "Consequences"):
            content += f"\n## {heading}\n\nRecorded fact.\n"
        self.write("implemented/2026-10-15-storage.md", content)
        self.assertEqual(validate_tree(self.root), ([], 1))


if __name__ == "__main__":
    unittest.main()
