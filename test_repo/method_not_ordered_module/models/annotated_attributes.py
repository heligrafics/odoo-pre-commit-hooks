from typing import ClassVar

from odoo import fields, models


class FooModel(models.Model):
    _name = "foo.model"
    _description = "Foo Model"

    name = fields.Char(string="Name", required=True)

    def create(self, vals):
        return super().create(vals)

    _inherit: ClassVar[list[str]] = ["mail.thread"]
