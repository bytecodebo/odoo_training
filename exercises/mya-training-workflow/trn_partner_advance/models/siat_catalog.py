from odoo import api, fields, models


class SiatDocumentType(models.Model):
    _name = 'siat.document.type'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Document Type'


class SiatUoM(models.Model):
    _name = 'siat.uom'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat UoM'




