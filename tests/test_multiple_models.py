import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src", "hg_odoo_pre_commit_hooks", "check_method_order.py")
TEST_REPO = os.path.join(BASE_DIR, "test_repo")


def test_multiple_models_error():
    """Check that multiple Odoo models in the same file are detected as an error."""
    path = os.path.join(
        TEST_REPO, "method_not_ordered_module", "models", "multiple_models.py"
    )
    result = subprocess.run(
        ["python", SRC, path],
        capture_output=True,
        text=True,
        check=False,
    )
    # Should fail
    assert result.returncode == 1
    # Should contain the multiple models error message
    assert "Multiple Odoo models found in the same file" in result.stdout
    assert "2 classes" in result.stdout
