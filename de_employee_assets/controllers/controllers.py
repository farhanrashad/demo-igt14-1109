# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeAssets(http.Controller):
#     @http.route('/de_employee_assets/de_employee_assets/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_assets/de_employee_assets/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_assets.listing', {
#             'root': '/de_employee_assets/de_employee_assets',
#             'objects': http.request.env['de_employee_assets.de_employee_assets'].search([]),
#         })

#     @http.route('/de_employee_assets/de_employee_assets/objects/<model("de_employee_assets.de_employee_assets"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_assets.object', {
#             'object': obj
#         })
