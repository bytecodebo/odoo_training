# -*- coding: utf-8 -*-
# from odoo import http


# class TrnMainSetting(http.Controller):
#     @http.route('/trn_main_setting/trn_main_setting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trn_main_setting/trn_main_setting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trn_main_setting.listing', {
#             'root': '/trn_main_setting/trn_main_setting',
#             'objects': http.request.env['trn_main_setting.trn_main_setting'].search([]),
#         })

#     @http.route('/trn_main_setting/trn_main_setting/objects/<model("trn_main_setting.trn_main_setting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trn_main_setting.object', {
#             'object': obj
#         })
