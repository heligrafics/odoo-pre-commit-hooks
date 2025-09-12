import pytest
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src", "hg_odoo_pre_commit_hooks", "check_method_order.py")


def run_validator(filepath):
    """Ejecuta el validador y devuelve (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["python", SRC, filepath],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def test_constrains_decorator_detection(tmp_path):
    """Test that both @api.constrains and @api.constraints decorators are correctly detected."""
    
    # Test with correct Odoo @api.constrains decorator
    constrains_file = tmp_path / "test_constrains.py"
    constrains_file.write_text("""
from odoo import api, fields, models

class TestModel(models.Model):
    _name = "test.model"
    
    name = fields.Char()
    
    @api.constrains("name")
    def _check_name(self):
        pass
""")
    
    rc, out, err = run_validator(str(constrains_file))
    # Should pass with no errors since methods are in correct order
    assert rc == 0, f"@api.constrains should be detected correctly. Output: {out}, Error: {err}"
    
    
    # Test with legacy @api.constraints decorator (for backward compatibility)
    constraints_file = tmp_path / "test_constraints.py"
    constraints_file.write_text("""
from odoo import api, fields, models

class TestModel(models.Model):
    _name = "test.model"
    
    name = fields.Char()
    
    @api.constraints("name")
    def _check_name(self):
        pass
""")
    
    rc, out, err = run_validator(str(constraints_file))
    # Should pass with no errors since methods are in correct order
    assert rc == 0, f"@api.constraints should be detected correctly for backward compatibility. Output: {out}, Error: {err}"


def test_constrains_out_of_order(tmp_path):
    """Test that @api.constrains methods are correctly categorized and order violations are detected."""
    
    # Test file with @api.constrains method out of order
    test_file = tmp_path / "test_out_of_order.py"
    test_file.write_text("""
from odoo import api, fields, models

class TestModel(models.Model):
    _name = "test.model"
    
    name = fields.Char()
    
    # This should come AFTER constraints methods according to EXPECTED_ORDER
    def create(self, vals):
        return super().create(vals)
    
    # This constrains method is out of order - should come before CRUD methods
    @api.constrains("name")
    def _check_name(self):
        pass
""")
    
    rc, out, err = run_validator(str(test_file))
    # Should fail due to order violation
    assert rc == 1, f"Should detect order violation. Output: {out}, Error: {err}"
    assert "_check_name" in out, f"Should mention the out-of-order constrains method. Output: {out}"
    assert "constraints_methods" in out, f"Should identify the method as constraints_methods. Output: {out}"