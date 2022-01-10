# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountBillTax(http.Controller):
#     @http.route('/de_account_bill_tax/de_account_bill_tax/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_bill_tax/de_account_bill_tax/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_bill_tax.listing', {
#             'root': '/de_account_bill_tax/de_account_bill_tax',
#             'objects': http.request.env['de_account_bill_tax.de_account_bill_tax'].search([]),
#         })

#     @http.route('/de_account_bill_tax/de_account_bill_tax/objects/<model("de_account_bill_tax.de_account_bill_tax"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_bill_tax.object', {
#             'object': obj
#         })
