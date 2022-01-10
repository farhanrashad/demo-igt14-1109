# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseRequisitionRef(http.Controller):
#     @http.route('/de_purchase_requisition_ref/de_purchase_requisition_ref/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_requisition_ref/de_purchase_requisition_ref/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_requisition_ref.listing', {
#             'root': '/de_purchase_requisition_ref/de_purchase_requisition_ref',
#             'objects': http.request.env['de_purchase_requisition_ref.de_purchase_requisition_ref'].search([]),
#         })

#     @http.route('/de_purchase_requisition_ref/de_purchase_requisition_ref/objects/<model("de_purchase_requisition_ref.de_purchase_requisition_ref"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_requisition_ref.object', {
#             'object': obj
#         })
