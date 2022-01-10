# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseTeam(http.Controller):
#     @http.route('/de_purchase_team/de_purchase_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_team/de_purchase_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_team.listing', {
#             'root': '/de_purchase_team/de_purchase_team',
#             'objects': http.request.env['de_purchase_team.de_purchase_team'].search([]),
#         })

#     @http.route('/de_purchase_team/de_purchase_team/objects/<model("de_purchase_team.de_purchase_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_team.object', {
#             'object': obj
#         })
