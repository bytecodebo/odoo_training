# -*- coding: utf-8 -*-
# from odoo import http


# class TrnExamenEjercicio(http.Controller):
#     @http.route('/trn_examen_ejercicio/trn_examen_ejercicio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_examen_ejercicio/trn_examen_ejercicio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_examen_ejercicio.listing', {
#             'root': '/trn_examen_ejercicio/trn_examen_ejercicio',
#             'objects': http.request.env['trn_examen_ejercicio.trn_examen_ejercicio'].search([]),
#         })

#     @http.route('/trn_examen_ejercicio/trn_examen_ejercicio/objects/<model("trn_examen_ejercicio.trn_examen_ejercicio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_examen_ejercicio.object', {
#             'object': obj
#         })
