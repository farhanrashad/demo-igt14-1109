# -*- coding: utf-8 -*-
# from odoo import http


# class OpenhcmEmployeeTraining(http.Controller):
#     @http.route('/openhcm_employee_training/openhcm_employee_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openhcm_employee_training/openhcm_employee_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openhcm_employee_training.listing', {
#             'root': '/openhcm_employee_training/openhcm_employee_training',
#             'objects': http.request.env['openhcm_employee_training.openhcm_employee_training'].search([]),
#         })

#     @http.route('/openhcm_employee_training/openhcm_employee_training/objects/<model("openhcm_employee_training.openhcm_employee_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openhcm_employee_training.object', {
#             'object': obj
#         })
