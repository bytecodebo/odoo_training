# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class trn_account_invoicing(models.Model):
#     _name = 'trn_account_invoicing.trn_account_invoicing'
#     _description = 'trn_account_invoicing.trn_account_invoicing'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
