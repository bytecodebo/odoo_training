import random
from datetime import timedelta

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'


    def _update_qty_on_hand_products(self, id_products=None, quantity=10):
        super()._update_qty_on_hand_products(id_products=id_products, quantity=quantity)
        if not id_products:
            id_products = [0]
        product_ids= self.env["product.product"].browse(id_products)
        for item in product_ids:
            action = item.product_tmpl_id.with_context(default_product_id=item.id,
                                                       create=True).action_update_quantity_on_hand()
            vals = {'product_id': item.id,
                    'product_tmpl_id': item.product_tmpl_id.id}
            wizard_id = self.env['stock.change.product.qty'].with_context(**action['context']).create(vals)
            wizard_id.new_quantity = quantity
            wizard_id.product_id = item
            wizard_id.change_product_qty()