import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class FooModel(models.Model):
    _name = "foo.model"
    _description = "Foo Model"
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    name = fields.Char(string="Name", required=True, default=lambda s: s._default_name())
    description = fields.Text(string="Description")
    value = fields.Integer(string="Value", default=0)

    @api.model
    def _default_name(self):
        return "Default Name"
