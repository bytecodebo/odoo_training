# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class trn_exam_partner_contact(models.Model):
#     _name = 'trn_exam_partner_contact.trn_exam_partner_contact'
#     _description = 'trn_exam_partner_contact.trn_exam_partner_contact'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
