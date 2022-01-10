# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseTeamAccount(http.Controller):
#     @http.route('/de_purchase_team_account/de_purchase_team_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_team_account/de_purchase_team_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_team_account.listing', {
#             'root': '/de_purchase_team_account/de_purchase_team_account',
#             'objects': http.request.env['de_purchase_team_account.de_purchase_team_account'].search([]),
#         })

#     @http.route('/de_purchase_team_account/de_purchase_team_account/objects/<model("de_purchase_team_account.de_purchase_team_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_team_account.object', {
#             'object': obj
#         })
