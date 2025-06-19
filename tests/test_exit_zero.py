import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src", "hg_odoo_pre_commit_hooks", "check_method_order.py")
TEST_REPO = os.path.join(BASE_DIR, "test_repo")


def test_exit_zero_flag_returns_zero_on_error():
    """If --exit-zero is passed, the script should return 0 even if errors are found."""
    path = os.path.join(
        TEST_REPO,
        "method_not_ordered_module",
        "models",
        "action_methods.py",
    )
    result = subprocess.run(
        ["python", SRC, "--exit-zero", path],
        capture_output=True,
        text=True,
        check=False,
    )
    assert not result.returncode
    assert "action_methods.py" in result.stdout or "action_methods.py" in result.stderr
