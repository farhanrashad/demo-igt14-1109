# -*- coding: utf-8 -*-
# from odoo import http


# class DeForceClose(http.Controller):
#     @http.route('/de_force_close/de_force_close/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_force_close/de_force_close/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_force_close.listing', {
#             'root': '/de_force_close/de_force_close',
#             'objects': http.request.env['de_force_close.de_force_close'].search([]),
#         })

#     @http.route('/de_force_close/de_force_close/objects/<model("de_force_close.de_force_close"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_force_close.object', {
#             'object': obj
#         })
