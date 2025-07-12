from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    #para implementar la restriccion de un cliente padre no puede tener como hijo a otro cliente padre
    #entonces añadiremos un campo booleano, por ejemplo is_parent_customer.
    is_parent_customer = fields.Boolean(string='¿Es Cliente Padre?')

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
            # Buscar el siguientee máximo consecutivo child_code entre los hijos que ya existen
            max_code = max(parent.child_ids.mapped('child_code') or [0])
            vals['child_code'] = max_code + 1
        return super(ResPartner, self).create(vals)

    #aqui comprobamos que un cliente padre no puede tener como hijo a otro cliente padre
    # al intentar asignar como padre a otro cliente que también es “cliente padre”, arrojará un error.
    @api.constrains('parent_id', 'is_parent_customer')
    def _check_parent_customer_constraint(self):
        for rec in self:
            if rec.parent_id and rec.parent_id.is_parent_customer and rec.is_parent_customer:
                raise ValidationError(
                    'Un cliente padre no puede tener como hijo a otro cliente padre.'
                )