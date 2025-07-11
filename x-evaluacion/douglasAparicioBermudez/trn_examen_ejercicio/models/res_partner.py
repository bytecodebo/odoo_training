from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    child_code = fields.Integer(
        string='Código correlativo',
        readonly=True,
        copy=False,
        help='Código correlativo único para hijos bajo el mismo cliente padre.'
    )

    @api.model
    def create(self, vals):
        if vals.get('parent_id'):
            parent = self.env['res.partner'].browse(vals['parent_id'])
            # Buscar el siguientee máximo child_code entre los hijos que ya existen
            max_code = max(parent.child_ids.mapped('child_code') or [0])
            vals['child_code'] = max_code + 1
        return super(ResPartner, self).create(vals)