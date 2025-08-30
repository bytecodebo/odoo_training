from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_parent_customer = fields.Boolean(
        string="¿Es cliente padre?",
        default=False
    )
    parent_customer_id = fields.Many2one(
        'res.partner',
        string="Cliente padre",
        domain="[('is_parent_customer', '=', True)]"
    )
    partner_code = fields.Char(
        string="Código del cliente",
        readonly=True,
        copy=False
    )

    @api.model
    def create(self, vals):
        is_parent = vals.get('is_parent_customer', False)
        parent_id = vals.get('parent_customer_id')

        if is_parent:
            last_parent = self.search(
                [('is_parent_customer', '=', True)],
                order='partner_code desc',
                limit=1
            )
            last_code = last_parent.partner_code if last_parent and last_parent.partner_code else 'CCP00000'
            new_num = int(last_code[3:]) + 1000
            vals['partner_code'] = f"CCP{str(new_num).zfill(5)}"

        elif parent_id:
            parent = self.env['res.partner'].browse(parent_id)
            if not parent.partner_code:
                raise ValidationError("Debe ingresar un cliente padre con un código válido antes de continuar.")
  
            siblings = self.search([
                ('parent_customer_id', '=', parent.id),
                ('partner_code', 'like', parent.partner_code[:6] + '%')
            ], order='partner_code desc', limit=1)

            if siblings and siblings.partner_code:
                last_suffix = int(siblings.partner_code[-2:])
                new_suffix = str(last_suffix + 1).zfill(2)
            else:
                new_suffix = "01"

            vals['partner_code'] = f"{parent.partner_code[:6]}{new_suffix}"

        return super().create(vals)

    @api.constrains('is_parent_customer', 'parent_customer_id')
    def _check_no_nested_parents(self):
        for rec in self:
            if rec.is_parent_customer and rec.parent_customer_id:
                raise ValidationError("Un cliente padre no puede tener un cliente padre.")
