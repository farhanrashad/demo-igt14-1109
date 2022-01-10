# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseOrderType(http.Controller):
#     @http.route('/de_purchase_order_type/de_purchase_order_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_order_type/de_purchase_order_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_order_type.listing', {
#             'root': '/de_purchase_order_type/de_purchase_order_type',
#             'objects': http.request.env['de_purchase_order_type.de_purchase_order_type'].search([]),
#         })

#     @http.route('/de_purchase_order_type/de_purchase_order_type/objects/<model("de_purchase_order_type.de_purchase_order_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_order_type.object', {
#             'object': obj
#         })
