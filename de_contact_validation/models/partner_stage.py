# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class PartnerStage(models.Model):
    _name = 'res.partner.stage'
    _description = 'Partner Stage'
    _order = 'sequence, stage_category, id'
    
    #def _get_default_custom_entry_type_ids(self):
        #default_custom_entry_type_id = self.env.context.get('default_custom_entry_type_id')
        #return [default_custom_entry_type_id] if default_custom_entry_type_id else None
    
    name = fields.Char(string='Stage Name', required=True, translate=True)
    stage_code = fields.Char(string='Code', size=3, copy=False)
    description = fields.Text(
        "Requirements", help="Enter here the internal requirements for this stage. It will appear "
                             "as a tooltip over the stage's name.", translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    category_ids = fields.Many2many('res.partner.category', column1='partner_id', column2='category_id', string='Categories')
    
    #custom_entry_type_ids = fields.Many2many('account.custom.entry.type', 'custom_entry_type_stage_rel', 'custom_entry_stage_id', 'custom_entry_type_id', string='Entry Types', default=_get_default_custom_entry_type_ids)
    
    stage_category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Category', default='draft')
    

    group_id = fields.Many2one('res.groups', string='Security Group')
    
    _sql_constraints = [
        ('code_uniq', 'unique (stage_code)', "Code already exists!"),
    ]

