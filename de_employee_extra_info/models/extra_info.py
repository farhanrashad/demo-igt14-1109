from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    employee_extra_info_line = fields.One2many('hr.employee.extra.info', 'extra_info')


class ExtraInfo(models.Model):
    _name = 'hr.employee.extra.info'
    _description = 'Employee Extra Info'

    extra_info = fields.Many2one('hr.employee', string='Extra Info')
    employee_info_type_id = fields.Many2one('hr.employee.extra.field.type', string='Field Type')
    name = fields.Char(string='Value')


class ExtraInfoFieldType(models.Model):
    _name = 'hr.employee.extra.field.type'
    _description = 'Employee Extra Info Field Type'

    name = fields.Char(string='Field')

