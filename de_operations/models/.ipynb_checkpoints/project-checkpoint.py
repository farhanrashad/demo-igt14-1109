# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast
from datetime import timedelta, datetime
from random import randint

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning
from odoo.tools.misc import format_date, get_lang
from odoo.osv.expression import OR

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    site_hoto = fields.Boolean(string='Is site HoTO project?')
    date_rfi = fields.Date(string='RFI Date')
    date_onair = fields.Date(string='On Air Date')
    date_handover = fields.Date(string='Handover Date')
    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    site_hoto = fields.Boolean(string='Is HOTO Task?')
    
    site_id = fields.Many2one('project.project', string='Site', index=True, tracking=True, check_company=True, change_default=True)
    hoto_type = fields.Selection([
        ('new', 'New RFI'),
        ('supplier', 'Supplier to Supplier'),
    ], default='new', string='HOTO Type')
    
    date_handover = fields.Date(string='Handover Date')
    date_rfi = fields.Date(string='RFI Date')
    date_onair = fields.Date(string='On Air Date')
    
    @api.onchange('site_hoto')
    def _find_hoto_project(self):
        for task in self:
            project_id = self.env['project.project'].search([('name','=','HOTO')],limit=1)
            if not project_id:
                project_id = self.env['project.project'].create({
                    'name':'HOTO',
                    'site_hoto':True,
                })
            task.project_id = project_id.id
            task.name = 'New HOTO'