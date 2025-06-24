from odoo import _, api, fields, models, tools

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    svl_grouped_move_purchase = fields.Boolean(string="Journal entry grouped for purchase")
    svl_grouped_move_sale = fields.Boolean(string="Journal entry grouped for sales")