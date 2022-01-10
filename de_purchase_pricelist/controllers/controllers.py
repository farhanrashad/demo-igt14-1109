# -*- coding: utf-8 -*-
# from odoo import http


# class DePurcahsePricelist(http.Controller):
#     @http.route('/de_purcahse_pricelist/de_purcahse_pricelist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purcahse_pricelist/de_purcahse_pricelist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purcahse_pricelist.listing', {
#             'root': '/de_purcahse_pricelist/de_purcahse_pricelist',
#             'objects': http.request.env['de_purcahse_pricelist.de_purcahse_pricelist'].search([]),
#         })

#     @http.route('/de_purcahse_pricelist/de_purcahse_pricelist/objects/<model("de_purcahse_pricelist.de_purcahse_pricelist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purcahse_pricelist.object', {
#             'object': obj
#         })
