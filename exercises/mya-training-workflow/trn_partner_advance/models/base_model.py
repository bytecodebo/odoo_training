from odoo import api, fields, models


class SiatCatalogMixin(models.AbstractModel):
    _name = 'siat.catalog.mixin'
    _description = 'Siat Catalog Mixin'
    _rec_name = 'description'
    _active_name = 'active'
    _enabled_name = 'enabled'
    _rec_names_search = ['code_classificator', 'description']

    def name_get(self):
        result = []
        for record in self:
            display_name = "[%s] %s" % (record.code_classificator, record.description)
            result.append((record.id, display_name))
        return result

    code_classificator = fields.Integer(string="Code", default=0, required=True, )
    description = fields.Char(string="Description", required=True, )
    enabled = fields.Boolean(default=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('posted', 'Posted'),
                                                        ('cancel', 'Cancelled')], required=True, default='draft')

    def action_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_to_post(self):
        for rec in self:
            rec.state = 'posted'

    def action_to_cancel(self):
        for rec in self:
            rec.state = 'cancel'

