# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductBarcode(http.Controller):
#     @http.route('/de_product_barcode/de_product_barcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_barcode/de_product_barcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_barcode.listing', {
#             'root': '/de_product_barcode/de_product_barcode',
#             'objects': http.request.env['de_product_barcode.de_product_barcode'].search([]),
#         })

#     @http.route('/de_product_barcode/de_product_barcode/objects/<model("de_product_barcode.de_product_barcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_barcode.object', {
#             'object': obj
#         })
