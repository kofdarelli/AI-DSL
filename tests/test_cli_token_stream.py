import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import main

class TestCLITokens(unittest.TestCase):
    def test_cli_tokens_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            sample_file = Path(tmp_dir) / "sample.dsl"
            sample_file.write_text('agent my_agent -> { task t = 42 } "hello"', encoding="utf-8")

            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                exit_code = main(["--token", str(sample_file)])

            self.assertEqual(exit_code, 0)
            output = mock_stdout.getvalue()
            
            self.assertIn("AGENT 'agent'", output)
            self.assertIn("IDENT 'my_agent'", output)
            self.assertIn("ARROW '->'", output)
            self.assertIn("INT_LITERAL '42'", output)
            self.assertIn("STRING_LITERAL '\"hello\"'", output)

    def test_cli_tokens_lexer_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_file = Path(tmp_dir) / "bad.dsl"
            bad_file.write_text("agent @", encoding="utf-8")

            with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
                exit_code = main(["--token", str(bad_file)])

            self.assertEqual(exit_code, 1)
            self.assertIn("Syntax error", mock_stderr.getvalue())

if __name__ == "__main__":
    unittest.main()