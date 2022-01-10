# -*- coding: utf-8 -*-
# from odoo import http


# class OpenhcmEmployeeAttendance(http.Controller):
#     @http.route('/openhcm_employee_attendance/openhcm_employee_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openhcm_employee_attendance/openhcm_employee_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openhcm_employee_attendance.listing', {
#             'root': '/openhcm_employee_attendance/openhcm_employee_attendance',
#             'objects': http.request.env['openhcm_employee_attendance.openhcm_employee_attendance'].search([]),
#         })

#     @http.route('/openhcm_employee_attendance/openhcm_employee_attendance/objects/<model("openhcm_employee_attendance.openhcm_employee_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openhcm_employee_attendance.object', {
#             'object': obj
#         })
