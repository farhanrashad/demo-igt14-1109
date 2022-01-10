# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning


class HrJob(models.Model):
    _inherit = 'hr.job'

    hired_id = fields.Integer(string='Hired Employee', compute='_compute_hired_employee')
    remaining_id = fields.Integer(string='Remaining Employee', compute='_compute_remaining_employee')

    @api.depends('hired_id')
    def _compute_hired_employee(self):
        for record in self:
            hired = self.env['hr.employee'].search_count([('job_title','=',record.name)])
#             raise UserError((hired.id))
            record.hired_id = hired
    
    @api.depends('hired_id')
    def _compute_remaining_employee(self):
        for record in self:
            record.remaining_id = self.no_of_recruitment - self.hired_id

