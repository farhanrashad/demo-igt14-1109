# coding: utf-8

from datetime import date
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
    
    
class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    project_id = fields.Many2one('project.project', string='Project')
    
    
    
        
    
