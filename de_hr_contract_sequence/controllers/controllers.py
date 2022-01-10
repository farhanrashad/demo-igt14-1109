# -*- coding: utf-8 -*-
# from odoo import http


# class DeContactSequence(http.Controller):
#     @http.route('/de_contact_sequence/de_contact_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_contact_sequence/de_contact_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_contact_sequence.listing', {
#             'root': '/de_contact_sequence/de_contact_sequence',
#             'objects': http.request.env['de_contact_sequence.de_contact_sequence'].search([]),
#         })

#     @http.route('/de_contact_sequence/de_contact_sequence/objects/<model("de_contact_sequence.de_contact_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_contact_sequence.object', {
#             'object': obj
#         })
