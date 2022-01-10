# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date



class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    #project_id = fields.Many2one('project.project', string='Project', compute='_assign_project', store=True, readonly=False, domain="[('allow_site_planning','=',True)]")
    project_id = fields.Many2one('project.project', string='Project')
    
    @api.depends('purchase_line_id')
    def _assign_project(self):
        if self.purchase_line_id:
            self.project_id = self.purchase_line_id.project_id.id
        
    @api.onchange('purchase_line_id')
    def onchange_purchase_line_id(self):
        if self.purchase_line_id:
            self.project_id = self.purchase_line_id.project_id.id