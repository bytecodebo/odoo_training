from odoo import _, api, fields, models, tools


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    svl_grouped_move_purchase = fields.Boolean(related="company_id.svl_grouped_move_purchase", readonly=False)
    svl_grouped_move_sale = fields.Boolean(related="company_id.svl_grouped_move_sale", readonly=False)
