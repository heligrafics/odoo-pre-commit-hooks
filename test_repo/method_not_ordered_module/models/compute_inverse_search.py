import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FooModel(models.Model):
    _name = "foo.model"
    _description = "Foo Model"

    name = fields.Char(
        string="Name", required=True, default=lambda s: s._default_name()
    )
    description = fields.Text(string="Description")
    value = fields.Integer(string="Value", default=0)
    selection_field = fields.Selection(
        selection=lambda self: self._selection_method(),
        string="Selection Field",
        default="option1",
    )
    computed_field = fields.Char(
        string="Computed Field",
        compute="_compute_inverse_search",
        inverse="_inverse_search_method",
    )

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The name must be unique."),
    ]

    @api.depends("value")
    def _compute_inverse_search(self):
        for record in self:
            record.computed_field = f"Computed Value: {record.value}"

    def _inverse_search_method(self):
        for record in self:
            # Example inverse logic, could be more complex
            record.value = (
                int(record.computed_field.split(": ")[-1])
                if record.computed_field
                else 0
            )

    @api.model
    def _default_name(self):
        return "Default Name"

    @api.model
    def _selection_method(self):
        return [
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
        ]
