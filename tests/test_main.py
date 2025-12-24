import tempfile
from pathlib import Path

from src.main import determine_output_file, sanitize_branch_name


def test_branch_name_sanitization() -> None:
    """Test that branch names are properly sanitized for filenames."""
    assert sanitize_branch_name("feature/new-feature") == "feature_new-feature"
    assert sanitize_branch_name("bug-fix#123") == "bug-fix_123"
    assert sanitize_branch_name("release/v1.0.0") == "release_v1.0.0"
    assert sanitize_branch_name("fix\\windows\\path") == "fix_windows_path"
    assert sanitize_branch_name("feat:add-login") == "feat_add-login"
    assert sanitize_branch_name("bug@123") == "bug_123"
    assert sanitize_branch_name("simple-branch") == "simple-branch"
    assert sanitize_branch_name("normal_branch") == "normal_branch"


def test_determine_output_file() -> None:
    """Test output file determination for different scenarios."""
    branch = "feature/test"

    # No output specified - should return default filename
    assert determine_output_file(None, branch) == "review_feature_test.md"

    # Specific file path specified - should return as-is
    assert determine_output_file("/tmp/custom.md", branch) == "/tmp/custom.md"

    # Directory specified - should append default filename
    with tempfile.TemporaryDirectory() as tmpdir:
        result = determine_output_file(tmpdir, branch)
        expected = str(Path(tmpdir) / "review_feature_test.md")
        assert result == expected
