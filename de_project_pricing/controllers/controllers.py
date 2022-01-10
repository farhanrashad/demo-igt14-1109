# -*- coding: utf-8 -*-
# from odoo import http


# class DeFuelProjectPricing(http.Controller):
#     @http.route('/de_fuel_project_pricing/de_fuel_project_pricing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_fuel_project_pricing/de_fuel_project_pricing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_fuel_project_pricing.listing', {
#             'root': '/de_fuel_project_pricing/de_fuel_project_pricing',
#             'objects': http.request.env['de_fuel_project_pricing.de_fuel_project_pricing'].search([]),
#         })

#     @http.route('/de_fuel_project_pricing/de_fuel_project_pricing/objects/<model("de_fuel_project_pricing.de_fuel_project_pricing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_fuel_project_pricing.object', {
#             'object': obj
#         })
