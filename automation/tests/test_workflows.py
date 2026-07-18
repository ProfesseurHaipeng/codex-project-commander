import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TRIAGE_WORKFLOW = ROOT / ".github/workflows/oss-maintainer-triage.yml"
PR_WORKFLOW = ROOT / ".github/workflows/oss-maintainer-pr.yml"
SCHEDULE_WORKFLOW = ROOT / ".github/workflows/oss-maintainer-schedule.yml"
WORKFLOWS = (TRIAGE_WORKFLOW, PR_WORKFLOW, SCHEDULE_WORKFLOW)


class WorkflowContractTests(unittest.TestCase):
    def test_no_workflow_has_contents_write(self):
        for path in WORKFLOWS:
            self.assertNotIn("contents: write", path.read_text(encoding="utf-8"))

    def test_pr_target_job_checks_out_only_trusted_default_branch(self):
        text = PR_WORKFLOW.read_text(encoding="utf-8")
        metadata = text.split("metadata:", 1)[1].split("checks:", 1)[0]
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", metadata)
        self.assertNotIn("github.event.pull_request.head.sha", metadata)

    def test_untrusted_checks_are_read_only(self):
        text = PR_WORKFLOW.read_text(encoding="utf-8")
        checks = text.split("checks:", 1)[1]
        self.assertIn("contents: read", checks)
        self.assertNotIn("issues: write", checks)
        self.assertNotIn("pull-requests: write", checks)

    def test_stale_schedule_is_manual_until_policy_enabled(self):
        text = SCHEDULE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("schedule:", text)

    def test_schedule_report_job_has_no_issue_write_or_apply_step(self):
        text = SCHEDULE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions: {}", text)
        self.assertNotIn("issues: write", text)
        self.assertNotIn("oss_maintainer.py apply", text)

    def test_openai_secret_is_absent_from_untrusted_checks(self):
        checks = PR_WORKFLOW.read_text(encoding="utf-8").split("checks:", 1)[1]
        self.assertNotIn("OPENAI_API_KEY", checks)
        self.assertNotIn("secrets.", checks)

    def test_all_action_references_are_immutable(self):
        for path in WORKFLOWS:
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses: actions/" in line:
                    reference = line.split("@", 1)[1].split()[0]
                    self.assertRegex(reference, r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
