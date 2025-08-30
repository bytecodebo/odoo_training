# -*- coding: utf-8 -*-
# from odoo import http


# class TrnExamPartnerContact(http.Controller):
#     @http.route('/trn_exam_partner_contact/trn_exam_partner_contact', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_exam_partner_contact/trn_exam_partner_contact/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_exam_partner_contact.listing', {
#             'root': '/trn_exam_partner_contact/trn_exam_partner_contact',
#             'objects': http.request.env['trn_exam_partner_contact.trn_exam_partner_contact'].search([]),
#         })

#     @http.route('/trn_exam_partner_contact/trn_exam_partner_contact/objects/<model("trn_exam_partner_contact.trn_exam_partner_contact"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_exam_partner_contact.object', {
#             'object': obj
#         })
