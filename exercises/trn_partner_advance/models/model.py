from odoo import fields, models, _



class ClassTesting(models.Model):
    _name = 'res.class.testing'
    _description = 'ClassTesting'

    name = fields.Char()

