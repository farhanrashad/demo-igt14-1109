# -*- coding: utf-8 -*-
# from odoo import http


# class DeBaseAddressExtended(http.Controller):
#     @http.route('/de_base_address_extended/de_base_address_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_base_address_extended/de_base_address_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_base_address_extended.listing', {
#             'root': '/de_base_address_extended/de_base_address_extended',
#             'objects': http.request.env['de_base_address_extended.de_base_address_extended'].search([]),
#         })

#     @http.route('/de_base_address_extended/de_base_address_extended/objects/<model("de_base_address_extended.de_base_address_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_base_address_extended.object', {
#             'object': obj
#         })
