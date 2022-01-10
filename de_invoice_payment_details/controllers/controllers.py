# -*- coding: utf-8 -*-
# from odoo import http


# class DeInvoicePaymentDetails(http.Controller):
#     @http.route('/de_invoice_payment_details/de_invoice_payment_details/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_invoice_payment_details/de_invoice_payment_details/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_invoice_payment_details.listing', {
#             'root': '/de_invoice_payment_details/de_invoice_payment_details',
#             'objects': http.request.env['de_invoice_payment_details.de_invoice_payment_details'].search([]),
#         })

#     @http.route('/de_invoice_payment_details/de_invoice_payment_details/objects/<model("de_invoice_payment_details.de_invoice_payment_details"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_invoice_payment_details.object', {
#             'object': obj
#         })
