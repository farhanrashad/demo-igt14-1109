# -*- coding: utf-8 -*-
# from odoo import http


# class DeVendorWarranty(http.Controller):
#     @http.route('/de_vendor_warranty/de_vendor_warranty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_vendor_warranty/de_vendor_warranty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_vendor_warranty.listing', {
#             'root': '/de_vendor_warranty/de_vendor_warranty',
#             'objects': http.request.env['de_vendor_warranty.de_vendor_warranty'].search([]),
#         })

#     @http.route('/de_vendor_warranty/de_vendor_warranty/objects/<model("de_vendor_warranty.de_vendor_warranty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_vendor_warranty.object', {
#             'object': obj
#         })
