from odoo import api, fields, models


class SiatDocumentType(models.Model):
    _name = 'siat.document.type'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Document Type'


class SiatUoM(models.Model):
    _name = 'siat.uom'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat UoM'

class SiatActivity(models.Model):
    _name = 'siat.activity'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Activity'

    caeb_code = fields.Char(string="CAEB Code", required=False, )
    activity_type = fields.Char()



