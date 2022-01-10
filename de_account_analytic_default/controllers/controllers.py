# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeAnalytic(http.Controller):
#     @http.route('/de_employee_analytic/de_employee_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_analytic/de_employee_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_analytic.listing', {
#             'root': '/de_employee_analytic/de_employee_analytic',
#             'objects': http.request.env['de_employee_analytic.de_employee_analytic'].search([]),
#         })

#     @http.route('/de_employee_analytic/de_employee_analytic/objects/<model("de_employee_analytic.de_employee_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_analytic.object', {
#             'object': obj
#         })
