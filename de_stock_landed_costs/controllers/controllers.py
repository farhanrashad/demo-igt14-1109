# -*- coding: utf-8 -*-
# from odoo import http


# class DeLandedCostProduct(http.Controller):
#     @http.route('/de_landed_cost_product/de_landed_cost_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_landed_cost_product/de_landed_cost_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_landed_cost_product.listing', {
#             'root': '/de_landed_cost_product/de_landed_cost_product',
#             'objects': http.request.env['de_landed_cost_product.de_landed_cost_product'].search([]),
#         })

#     @http.route('/de_landed_cost_product/de_landed_cost_product/objects/<model("de_landed_cost_product.de_landed_cost_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_landed_cost_product.object', {
#             'object': obj
#         })
