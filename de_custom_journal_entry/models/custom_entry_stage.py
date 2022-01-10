# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class AccountCustomEntryStage(models.Model):
    _name = 'account.custom.entry.stage'
    _description = 'Custom Entry Stage'
    _order = 'sequence, stage_category, id'

    def _get_default_custom_entry_type_ids(self):
        default_custom_entry_type_id = self.env.context.get('default_custom_entry_type_id')
        return [default_custom_entry_type_id] if default_custom_entry_type_id else None
    
    name = fields.Char(string='Stage Name', required=True, translate=True)
    stage_code = fields.Char(string='Code', size=3, copy=False)
    active = fields.Boolean(default=True)
    description = fields.Text(
        "Requirements", help="Enter here the internal requirements for this stage. It will appear "
                             "as a tooltip over the stage's name.", translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    custom_entry_type_ids = fields.Many2many('account.custom.entry.type', 'custom_entry_type_stage_rel', 'custom_entry_stage_id', 'custom_entry_type_id', string='Entry Types',
        default=_get_default_custom_entry_type_ids)
    
    stage_category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('confirm', 'Confirmed'),
        ('closed', 'Closed'),
    ], string='Category', default='draft')
    
    account_entry_type = fields.Selection([
        ('none', 'None'),
        ('payment', 'Payment'),
        ('bill', 'Bill'),
        ('entry', 'Journal Entry'),
    ], string='Accounting Entry', default='none')
    
    next_stage_id = fields.Many2one('account.custom.entry.stage', string='Next Stage' )
    prv_stage_id = fields.Many2one('account.custom.entry.stage', string='Previous Stage')

    group_id = fields.Many2one('res.groups', string='Security Group')
    allow_editing = fields.Boolean(string='Allow Editing')
    _sql_constraints = [
        ('code_uniq', 'unique (stage_code)', "Code already exists!"),
    ]

