"""Tests for CLI input-file validation.

A directory (or a missing path) passed as the input file must fail with a
clean one-line error and exit code 1 -- never a traceback.
"""

from md2pdf.cli import main


class TestCliInputValidation:
    def test_directory_input_fails_cleanly(self, tmp_path, capsys, monkeypatch):
        """Passing a directory must error cleanly without a traceback."""
        monkeypatch.setattr("sys.argv", ["md2pdf", str(tmp_path)])
        assert main() == 1
        captured = capsys.readouterr()
        assert "directory" in captured.err.lower()
        assert "Traceback" not in captured.err

    def test_missing_file_fails_cleanly(self, tmp_path, capsys, monkeypatch):
        """Passing a missing file must error cleanly without a traceback."""
        missing = tmp_path / "does-not-exist.md"
        monkeypatch.setattr("sys.argv", ["md2pdf", str(missing)])
        assert main() == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower()
        assert "Traceback" not in captured.err
