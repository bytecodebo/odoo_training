# -*- coding: utf-8 -*-
# from odoo import http


# class TrnPartnerAdvance(http.Controller):
#     @http.route('/trn_partner_advance/trn_partner_advance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_partner_advance/trn_partner_advance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_partner_advance.listing', {
#             'root': '/trn_partner_advance/trn_partner_advance',
#             'objects': http.request.env['trn_partner_advance.trn_partner_advance'].search([]),
#         })

#     @http.route('/trn_partner_advance/trn_partner_advance/objects/<model("trn_partner_advance.trn_partner_advance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_partner_advance.object', {
#             'object': obj
#         })
