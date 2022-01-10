# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseRequisitionTemplate(http.Controller):
#     @http.route('/de_purchase_requisition_template/de_purchase_requisition_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_requisition_template/de_purchase_requisition_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_requisition_template.listing', {
#             'root': '/de_purchase_requisition_template/de_purchase_requisition_template',
#             'objects': http.request.env['de_purchase_requisition_template.de_purchase_requisition_template'].search([]),
#         })

#     @http.route('/de_purchase_requisition_template/de_purchase_requisition_template/objects/<model("de_purchase_requisition_template.de_purchase_requisition_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_requisition_template.object', {
#             'object': obj
#         })
