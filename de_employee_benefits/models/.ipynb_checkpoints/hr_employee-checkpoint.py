# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.employee'
    
    type = fields.Selection([
        ('expat', 'Expat'),
        ('local', 'Local'),
    ], default=False,  string='Type', help="Technical field for UX purpose.")
    
    
   