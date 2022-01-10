# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class EmployeeTrainingCourseMethod(models.Model):
    _name = 'hr.employee.training.course.delivery.method'
    _description = 'HR Employee Training Methods'
    _order = 'name desc'


    name = fields.Char(string='Name', store=True, required=True)

class EmployeeTrainingCourse(models.Model):
    _name = 'hr.employee.training.course'
    _description = 'HR Employee Training Course'
    _order = 'name desc'


    name = fields.Char(string='Name', store=True, required=True)
    employee_id = fields.Many2one('hr.employee',string='Coordinator', store=True, required=True)
    company_id = fields.Many2one('res.partner',string='Company', store=True)
    trainer_id = fields.Many2one('res.partner', string='Trainer', store=True, required=True)
    currency_id = fields.Many2one('res.currency',string='Currency', store=True)
    amount = fields.Float(string='Cost')
    note = fields.Html(string='Description')

    

    
