# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class trn_examen_ejercicio(models.Model):
#     _name = 'trn_examen_ejercicio.trn_examen_ejercicio'
#     _description = 'trn_examen_ejercicio.trn_examen_ejercicio'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
