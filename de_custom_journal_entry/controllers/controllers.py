# -*- coding: utf-8 -*-
# from odoo import http


# class DeCustomEntry(http.Controller):
#     @http.route('/de_custom_entry/de_custom_entry/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_custom_entry/de_custom_entry/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_custom_entry.listing', {
#             'root': '/de_custom_entry/de_custom_entry',
#             'objects': http.request.env['de_custom_entry.de_custom_entry'].search([]),
#         })

#     @http.route('/de_custom_entry/de_custom_entry/objects/<model("de_custom_entry.de_custom_entry"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_custom_entry.object', {
#             'object': obj
#         })
