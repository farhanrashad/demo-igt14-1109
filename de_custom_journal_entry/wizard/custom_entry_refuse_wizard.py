# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class CustomEntryRefuse(models.TransientModel):
    _name = 'custom.entry.refuse.wizard'
    _description = 'Custom Entry Refuse Wizard'

    custom_entry_id = fields.Many2one('account.custom.entry', 'Custom Entry')
    reason = fields.Text(string='Reason')
    
    
    def action_refuse(self):
        self.custom_entry_id.update({
            'text': self.reason,
            'stage_id' : self.custom_entry_id.stage_id.prv_stage_id.id,
        })    
    
    