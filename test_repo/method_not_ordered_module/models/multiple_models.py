import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FirstModel(models.Model):
    _name = "first.model"
    _description = "First Model"

    name = fields.Char(string="Name")


class SecondModel(models.Model):
    _name = "second.model"
    _description = "Second Model"

    name = fields.Char(string="Name")
