# -*- coding: utf-8 -*-
# from odoo import http


# class TrnAccountInvoicing(http.Controller):
#     @http.route('/trn_account_invoicing/trn_account_invoicing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_account_invoicing/trn_account_invoicing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_account_invoicing.listing', {
#             'root': '/trn_account_invoicing/trn_account_invoicing',
#             'objects': http.request.env['trn_account_invoicing.trn_account_invoicing'].search([]),
#         })

#     @http.route('/trn_account_invoicing/trn_account_invoicing/objects/<model("trn_account_invoicing.trn_account_invoicing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_account_invoicing.object', {
#             'object': obj
#         })
