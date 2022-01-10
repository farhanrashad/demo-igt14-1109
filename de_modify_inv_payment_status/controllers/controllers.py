# -*- coding: utf-8 -*-
# from odoo import http


# class DeModifyInvPaymentStatus(http.Controller):
#     @http.route('/de_modify_inv_payment_status/de_modify_inv_payment_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_modify_inv_payment_status/de_modify_inv_payment_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_modify_inv_payment_status.listing', {
#             'root': '/de_modify_inv_payment_status/de_modify_inv_payment_status',
#             'objects': http.request.env['de_modify_inv_payment_status.de_modify_inv_payment_status'].search([]),
#         })

#     @http.route('/de_modify_inv_payment_status/de_modify_inv_payment_status/objects/<model("de_modify_inv_payment_status.de_modify_inv_payment_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_modify_inv_payment_status.object', {
#             'object': obj
#         })
