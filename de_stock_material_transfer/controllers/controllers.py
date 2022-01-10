# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockRequisition(http.Controller):
#     @http.route('/de_stock_requisition/de_stock_requisition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_requisition/de_stock_requisition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_requisition.listing', {
#             'root': '/de_stock_requisition/de_stock_requisition',
#             'objects': http.request.env['de_stock_requisition.de_stock_requisition'].search([]),
#         })

#     @http.route('/de_stock_requisition/de_stock_requisition/objects/<model("de_stock_requisition.de_stock_requisition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_requisition.object', {
#             'object': obj
#         })
