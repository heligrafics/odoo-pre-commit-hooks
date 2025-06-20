import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src", "hg_odoo_pre_commit_hooks", "check_method_order.py")
TEST_REPO = os.path.join(BASE_DIR, "test_repo")


def test_several_errors_reports_all():
    """Check that all ordering errors in several_errors.py are reported."""
    path = os.path.join(
        TEST_REPO, "method_not_ordered_module", "models", "several_errors.py"
    )
    result = subprocess.run(
        ["python", SRC, path],
        capture_output=True,
        text=True,
        check=False,
    )
    # Should fail
    assert result.returncode == 1
    # Should report more than one error (at least two lines with 'appears out of order')
    error_lines = [
        line for line in result.stdout.splitlines() if "appears out of order" in line
    ]
    assert len(error_lines) >= 2, f"Expected multiple errors, got: {error_lines}"
