# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseBudgetRequisition(http.Controller):
#     @http.route('/de_purchase_budget_requisition/de_purchase_budget_requisition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_budget_requisition/de_purchase_budget_requisition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_budget_requisition.listing', {
#             'root': '/de_purchase_budget_requisition/de_purchase_budget_requisition',
#             'objects': http.request.env['de_purchase_budget_requisition.de_purchase_budget_requisition'].search([]),
#         })

#     @http.route('/de_purchase_budget_requisition/de_purchase_budget_requisition/objects/<model("de_purchase_budget_requisition.de_purchase_budget_requisition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_budget_requisition.object', {
#             'object': obj
#         })
