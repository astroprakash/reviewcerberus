from src.agent.tools.get_commit_messages import _get_commit_messages_impl
from tests.test_helper import create_test_repo


def test_get_commit_messages() -> None:
    with create_test_repo() as repo_path:
        result = _get_commit_messages_impl(str(repo_path), "main")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].message == "Add feature"
        assert result[0].author == "Test User"
