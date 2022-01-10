from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    active_emp = fields.Boolean(string='Active Emp')
   