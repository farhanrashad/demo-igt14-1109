# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountFinPeriod(http.Controller):
#     @http.route('/de_account_fin_period/de_account_fin_period/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_fin_period/de_account_fin_period/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_fin_period.listing', {
#             'root': '/de_account_fin_period/de_account_fin_period',
#             'objects': http.request.env['de_account_fin_period.de_account_fin_period'].search([]),
#         })

#     @http.route('/de_account_fin_period/de_account_fin_period/objects/<model("de_account_fin_period.de_account_fin_period"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_fin_period.object', {
#             'object': obj
#         })
