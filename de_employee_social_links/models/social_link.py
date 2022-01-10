# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Many2one


class EmployeeSocialLink(models.Model):
    _name = "hr.employee.social.link"

    
#   declaring fields 
#     name_des = fields.Char(string="Name",required=True)
    name =fields.Many2one('hr.employee.social.type', string="Social", required=True)
    social_icon = fields.Binary(related='name.social_icon',string="Icon",)
    social_link = fields.Char(string="Social Profile Link", required=True)
    employee_id =fields.Many2one('hr.employee')




class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    social_link_ids = fields.One2many('hr.employee.social.link', 'employee_id')

    
class HrEmployeeType(models.Model):
    _name = "hr.employee.social.type"
    _description = "Employee Social Types"
    
    name = fields.Char(string="Name", required=True)
    social_icon = fields.Binary(string="Social Icon", required=True)
    
    