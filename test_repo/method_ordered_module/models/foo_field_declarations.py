import logging

from odoo import api, fields, models
from odoo.addons.base_graph.models import graph_fields
from odoo.addons.base_json.models import json_fields
from odoo.addons.base_map.models import geospatial_fields

_logger = logging.getLogger(__name__)


class FooModel(models.Model):
    _name = "foo.model"
    _description = "Foo Model"

    asdf = fields.Char(string="Asdf", required=True)
    graph_field = graph_fields.Graph()
    json_field = json_fields.Json()
    geospatial_field = geospatial_fields.GeoField(dim="4")
    name = fields.Char(string="Name", required=True)
