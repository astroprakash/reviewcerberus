from src.agent.tools.diff_file import _diff_file_impl
from tests.test_helper import create_test_repo


def test_diff_file() -> None:
    with create_test_repo() as repo_path:
        result = _diff_file_impl(str(repo_path), "main", "file1.py")

        assert result.file_path == "file1.py"
        assert result.additions > 0
        assert result.deletions > 0
        assert "hello world" in result.diff
        assert result.total_hunks >= 1
