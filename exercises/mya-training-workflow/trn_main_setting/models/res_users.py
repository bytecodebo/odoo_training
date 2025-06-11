from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'


    def _create_user_from_template(self, values):
        pass