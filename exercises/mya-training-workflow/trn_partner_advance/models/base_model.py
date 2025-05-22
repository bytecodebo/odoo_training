from odoo import api, fields, models


class SiatCatalogMixin(models.AbstractModel):
    _name = 'siat.catalog.mixin'
    _description = 'Siat Catalog Mixin'

    code_classificator = fields.Integer(string="Code", default=0, required=True, )
    description = fields.Char(string="Description", required=True, )

