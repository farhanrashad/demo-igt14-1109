from odoo import models, fields


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    overtime_type_id = fields.Many2one('hr.overtime.type', string='Overtime Type')

