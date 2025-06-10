import random
from datetime import timedelta

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    mya_mng_pricelist_by_customer = fields.Boolean(default=False)

    def action_update_quantity_on_hand(self, product_ids=None, qty=10000):
        if product_ids:
            product_ids = self.env['product.product'].browse(product_ids)
        if not product_ids:
            product_ids = self.env['product.product'].search([('company_id', 'in', [False, self.id])])

        # for item in product_ids:
        #     action = item.product_tmpl_id.with_context(default_product_id=item.id,
        #                                                create=True).action_update_quantity_on_hand()
        #     vals = {'product_id': item.id}
        #     wizard_id = self.env['stock.change.product.qty'].with_context(**action['context']).create(vals)
        #     wizard_id.new_quantity = qty
        #     wizard_id.product_id = item
        #     wizard_id.change_product_qty()
        return {'type': 'ir.actions.act_window_close'}


    def action_update_pricelist(self):
        pricelist_id = self.env['product.pricelist'].search([('company_id', 'in', [False, self.id])], limit=1)
        if pricelist_id:
            product_ids = self.env['product.product'].search([('company_id', 'in', [False, self.id])])
            product_items = pricelist_id.item_ids.mapped('product_id')
            residual_prds = product_ids - product_items
            for item in residual_prds:
                vals = {
                    'applied_on': '1_product',
                    'product_tmpl_id': item.product_tmpl_id.id,
                    'fixed_price': random.randint(150, 1500) * 0.99
                }
                self.env['product.pricelist.item'].create(vals)

    def action_update_sale_orders_demo(self, start_date, interval=2, user_ids=None, max_orders=10):
        domain = [('date_order', '>=', start_date), ('company_id', 'in', [False, self.id])]
        if user_ids:
            domain += [('user_id', 'in', user_ids)]
        order_ids = self.env['sale.order'].search(domain, limit=max_orders)
        if order_ids:
            aux_date = start_date
            for order in order_ids:
                order.date_order = start_date
                start_date = start_date + timedelta(days=interval)
        return True

    def action_create_products_demo(self):
        product_ids = self.env["product.template"].search(
            [("company_id", "=", self.env.company.id)]
        )
        max_qty = 50
        init = len(product_ids)
        vals = []
        for x in range(init, init + max_qty):
            val = {
                "name": "Producto %s" % (x + 100),
                "default_code": (x + 100),
                "categ_id": self.env.ref("product.product_category_1").id,
                "type": "consu",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "uom_po_id": self.env.ref("uom.product_uom_unit").id,
                "list_price": random.randint(5, x + 20),
                "company_id": self.id,
            }
            vals.append(val)
        self.env["product.template"].sudo().create(vals)
        return True

    def action_delete_sale_order_data(self):
        domain_pos = [('company_id', 'in', [False, self.id])]
        sale_order_ids = self.env['sale.order'].search(domain_pos)

        move_ids = sale_order_ids.mapped('invoice_ids')
        move_ids.sudo().write({'state': 'cancel', 'posted_before': False})
        move_ids.line_ids.remove_move_reconcile()
        move_ids.sudo().unlink()
        # sale_order_ids.payment_ids.sudo().unlink()
        sale_order_ids.sudo().write({'state': 'cancel'})
        sale_order_ids.sudo().unlink()
        # stock_move_ids = self.env['stock.move'].search(domain_pos)
        # stock_move_ids.sudo().write({'state': 'cancel'})
        # stock_move_ids.sudo().write({'state': 'draft'})
        # stock_move_ids.sudo().unlink()
        # stock_picking_ids = self.env['stock.picking'].search(domain_pos)
        # stock_picking_ids.sudo().write({'state': 'cancel'})
        # stock_picking_ids.sudo().unlink()
        return True


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    test_start_date = fields.Datetime()
    mya_mng_pricelist_by_customer = fields.Boolean(related='company_id.mya_mng_pricelist_by_customer', readonly=False)

    def action_update_quantity_on_hand(self):
        return self.company_id.action_update_quantity_on_hand()

    def action_update_pricelist(self):
        return self.company_id.action_update_pricelist()

    def action_update_sale_orders_demo(self):
        start_date = fields.Datetime.now() - timedelta(days=30)
        return self.company_id.action_update_sale_orders_demo(start_date, max_orders=25)

    def action_delete_sale_order_data(self):
        return self.company_id.action_delete_sale_order_data()

    def action_create_products_demo(self):
        self.company_id.action_create_products_demo()
