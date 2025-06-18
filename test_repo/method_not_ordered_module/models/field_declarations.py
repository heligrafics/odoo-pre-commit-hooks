import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class FooModel(models.Model):
    description = fields.Text(string="Description")
    _name = "foo.model"
    _description = "Foo Model"

    name = fields.Char(string="Name", required=True, default=lambda s: s._default_name())

    @api.model
    def _default_name(self):
        return "Default Name"

    value = fields.Integer(string="Value", default=0)
