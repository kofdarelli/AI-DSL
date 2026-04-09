from __future__ import annotations

from pathlib import Path
import unittest

from src.docgen import main as docgen_main
from src.parser import DSLSyntaxError, syntax_check


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "examples" / "valid"
INVALID_DIR = ROOT / "examples" / "invalid"


class ParserExampleTests(unittest.TestCase):
    def test_valid_examples_parse(self) -> None:
        for path in sorted(VALID_DIR.glob("*.dsl")):
            with self.subTest(path=path.name):
                result = syntax_check(path)
                self.assertGreater(result.token_count, 0)

    def test_invalid_examples_fail(self) -> None:
        for path in sorted(INVALID_DIR.glob("*.dsl")):
            with self.subTest(path=path.name):
                with self.assertRaises(DSLSyntaxError):
                    syntax_check(path)

    def test_generated_docs_are_current(self) -> None:
        self.assertEqual(docgen_main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
