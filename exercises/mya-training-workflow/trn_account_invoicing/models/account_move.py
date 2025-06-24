from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    business_name = fields.Char()
    vat = fields.Char()
