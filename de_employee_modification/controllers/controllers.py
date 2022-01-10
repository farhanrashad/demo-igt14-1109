# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeModification(http.Controller):
#     @http.route('/de_employee_modification/de_employee_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_modification/de_employee_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_modification.listing', {
#             'root': '/de_employee_modification/de_employee_modification',
#             'objects': http.request.env['de_employee_modification.de_employee_modification'].search([]),
#         })

#     @http.route('/de_employee_modification/de_employee_modification/objects/<model("de_employee_modification.de_employee_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_modification.object', {
#             'object': obj
#         })
