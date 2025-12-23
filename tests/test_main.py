from src.main import sanitize_branch_name


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
