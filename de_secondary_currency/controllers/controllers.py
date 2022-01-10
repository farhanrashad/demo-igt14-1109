# -*- coding: utf-8 -*-
# from odoo import http


# class DeSecondaryCurrency(http.Controller):
#     @http.route('/de_secondary_currency/de_secondary_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_secondary_currency/de_secondary_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_secondary_currency.listing', {
#             'root': '/de_secondary_currency/de_secondary_currency',
#             'objects': http.request.env['de_secondary_currency.de_secondary_currency'].search([]),
#         })

#     @http.route('/de_secondary_currency/de_secondary_currency/objects/<model("de_secondary_currency.de_secondary_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_secondary_currency.object', {
#             'object': obj
#         })
