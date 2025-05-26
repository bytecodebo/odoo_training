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


class SiatPaymentMethod(models.Model):
    _name = 'siat.payment.method'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Payments'


class SiatCountry(models.Model):
    _name = 'siat.country'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Country'


class SiatCurrency(models.Model):
    _name = 'siat.currency'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat Currency'


class SiatPosType(models.Model):
    _name = 'siat.pos.type'
    _inherit = 'siat.catalog.mixin'
    _description = 'Siat POS Type'

