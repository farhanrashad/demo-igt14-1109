# -*- coding: utf-8 -*-
# from odoo import http


# class DeFuelManagement(http.Controller):
#     @http.route('/de_fuel_management/de_fuel_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_fuel_management/de_fuel_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_fuel_management.listing', {
#             'root': '/de_fuel_management/de_fuel_management',
#             'objects': http.request.env['de_fuel_management.de_fuel_management'].search([]),
#         })

#     @http.route('/de_fuel_management/de_fuel_management/objects/<model("de_fuel_management.de_fuel_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_fuel_management.object', {
#             'object': obj
#         })
