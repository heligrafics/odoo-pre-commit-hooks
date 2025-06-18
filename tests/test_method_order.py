import os
import subprocess

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src", "hg_odoo_pre_commit_hooks", "check_method_order.py")
TEST_REPO = os.path.join(BASE_DIR, "test_repo")


def run_validator(filepath):
    """Ejecuta el validador y devuelve (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["python", SRC, filepath],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.parametrize(
    "filename",
    [
        "private_attributes.py",
        "default_methods.py",
        "field_declarations.py",
        "sql_constraints.py",
        "selection_computed_methods.py",
        "compute_inverse_search.py",
        "constraints_methods.py",
        "onchange_methods.py",
        "crud_methods.py",
        "action_methods.py",
        "other_methods.py",
    ],
)
def test_not_ordered_models_fail(filename):
    """Los modelos desordenados deben fallar y mostrar el nombre del archivo."""
    path = os.path.join(TEST_REPO, "method_not_ordered_module", "models", filename)
    rc, out, err = run_validator(path)
    assert rc == 1
    assert filename in out or filename in err


def test_ordered_model_passes():
    """El modelo ordenado no debe dar error."""
    path = os.path.join(TEST_REPO, "method_ordered_module", "models", "model.py")
    rc, out, err = run_validator(path)
    assert not rc
    assert not out.strip()
    assert not err.strip()
