# -*- coding: utf-8 -*-
# from odoo import http


# class DeHrEmployeeVisa(http.Controller):
#     @http.route('/de_hr_employee_visa/de_hr_employee_visa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_hr_employee_visa/de_hr_employee_visa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_hr_employee_visa.listing', {
#             'root': '/de_hr_employee_visa/de_hr_employee_visa',
#             'objects': http.request.env['de_hr_employee_visa.de_hr_employee_visa'].search([]),
#         })

#     @http.route('/de_hr_employee_visa/de_hr_employee_visa/objects/<model("de_hr_employee_visa.de_hr_employee_visa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_hr_employee_visa.object', {
#             'object': obj
#         })
