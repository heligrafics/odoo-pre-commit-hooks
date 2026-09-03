from typing import ClassVar

from odoo import fields, models


class FooModel(models.Model):
    _name = "foo.model"
    _inherit: ClassVar[list[str]] = ["mail.thread"]
    _description = "Foo Model"

    CLASS_CONSTANT: ClassVar[str] = "CLASS CONSTANT"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    def action_reset_name(self):
        self.name = ""
