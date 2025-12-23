from src.agent.tools.search_in_files import _search_in_files_impl
from tests.test_helper import create_test_repo


def test_search_in_files() -> None:
    with create_test_repo() as repo_path:
        result = _search_in_files_impl(str(repo_path), "def")

        assert isinstance(result, list)
        assert len(result) > 0
        assert any("def" in m.line_content for m in result)
