import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README_FILES = (ROOT / "README.md", ROOT / "README.en.md")
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
SECURITY = ROOT / "SECURITY.md"
DOCUMENTS = (*README_FILES, CONTRIBUTING, SECURITY)


def read_document(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


class RepositoryDocumentationContractTests(unittest.TestCase):
    def test_readmes_discover_both_automated_maintenance_skills(self):
        for path in README_FILES:
            text = read_document(path)
            self.assertIn("`skills/automate-oss-maintenance`", text, path.name)
            self.assertIn("`skills/automate-oss-maintenance-zh`", text, path.name)

    def test_contributing_explains_automation_and_human_review(self):
        text = read_document(CONTRIBUTING)
        self.assertIn("automated replies", text.lower())
        self.assertIn("human review", text.lower())

    def test_security_names_private_vulnerability_reporting(self):
        self.assertIn("GitHub Private Vulnerability Reporting", read_document(SECURITY))

    def test_docs_do_not_claim_unverified_activation_or_adoption(self):
        forbidden_claims = (
            "active workflow",
            "active workflows",
            "externally adopted",
            "external adoption",
        )
        for path in DOCUMENTS:
            text = read_document(path).lower()
            for claim in forbidden_claims:
                self.assertNotIn(claim, text, f"{path.name}: {claim}")


if __name__ == "__main__":
    unittest.main()
