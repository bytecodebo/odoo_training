from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def action_create_partner_demo(self):
        self.company_id.partner_id.action_create_partner_demos()
