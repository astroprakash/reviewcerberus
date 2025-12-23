from src.agent.tools.changed_files import _changed_files_impl
from tests.test_helper import create_test_repo


def test_changed_files() -> None:
    with create_test_repo() as repo_path:
        result = _changed_files_impl(str(repo_path), "main")

        assert isinstance(result, list)
        assert len(result) == 2

        file1 = next(f for f in result if f.path == "file1.py")
        assert file1.change_type == "modified"
        assert file1.additions > 0
        assert file1.deletions > 0

        file3 = next(f for f in result if f.path == "file3.py")
        assert file3.change_type == "added"
        assert file3.additions > 0
        assert file3.deletions == 0
