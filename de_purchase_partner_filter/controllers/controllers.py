# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchasePartnerFilter(http.Controller):
#     @http.route('/de_purchase_partner_filter/de_purchase_partner_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_partner_filter/de_purchase_partner_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_partner_filter.listing', {
#             'root': '/de_purchase_partner_filter/de_purchase_partner_filter',
#             'objects': http.request.env['de_purchase_partner_filter.de_purchase_partner_filter'].search([]),
#         })

#     @http.route('/de_purchase_partner_filter/de_purchase_partner_filter/objects/<model("de_purchase_partner_filter.de_purchase_partner_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_partner_filter.object', {
#             'object': obj
#         })
