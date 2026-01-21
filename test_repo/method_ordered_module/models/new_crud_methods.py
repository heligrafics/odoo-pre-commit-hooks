from odoo import models


class NewCrudInfo(models.Model):
    _name = "new.crud.info"
    _description = "New Crud Info"

    # CRUD methods (order 9)
    def search_read(self):
        pass

    def search_fetch(self):
        pass

    def browse(self):
        pass

    def read_group(self):
        pass

    def toggle_active(self):
        pass

    # Action methods (order 10)
    def action_foo(self):
        pass
