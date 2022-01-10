# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
    
    
class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    employee_id = fields.Many2one('hr.employee', string='Employee', )
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')
    project_id = fields.Many2one('project.project', string='Project', )