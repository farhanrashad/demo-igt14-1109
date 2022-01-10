# -*- coding: utf-8 -*-
# from odoo import http


# class DeOperations(http.Controller):
#     @http.route('/de_operations/de_operations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_operations/de_operations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_operations.listing', {
#             'root': '/de_operations/de_operations',
#             'objects': http.request.env['de_operations.de_operations'].search([]),
#         })

#     @http.route('/de_operations/de_operations/objects/<model("de_operations.de_operations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_operations.object', {
#             'object': obj
#         })
