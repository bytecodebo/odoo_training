# -*- coding: utf-8 -*-
# from odoo import http


# class TrnSaleOrder(http.Controller):
#     @http.route('/trn_sale_order/trn_sale_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_sale_order/trn_sale_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_sale_order.listing', {
#             'root': '/trn_sale_order/trn_sale_order',
#             'objects': http.request.env['trn_sale_order.trn_sale_order'].search([]),
#         })

#     @http.route('/trn_sale_order/trn_sale_order/objects/<model("trn_sale_order.trn_sale_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_sale_order.object', {
#             'object': obj
#         })
