import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class FooModel(models.Model):

    _name = "foo.model"
    _description = "Foo Model"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    value = fields.Integer(string="Value", default=0)

    CLASS_CONSTANT = "CLASS CONSTANT"
