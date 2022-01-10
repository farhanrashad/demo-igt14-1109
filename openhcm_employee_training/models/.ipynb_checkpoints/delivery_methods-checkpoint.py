# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DeliveryMethod(models.Model):
    _name = "hr.employee.training.course.delivery.method"
    _description = 'Employee Training Course Deivery Method'


    name= fields.Char(string='Delivery Method',required=True)


