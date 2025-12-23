from src.agent.tools.list_files import _list_files_impl
from tests.test_helper import create_test_repo


def test_list_files() -> None:
    with create_test_repo() as repo_path:
        result = _list_files_impl(str(repo_path))

        assert isinstance(result, list)
        assert "file1.py" in result
        assert "file3.py" in result
        assert len(result) == 3
