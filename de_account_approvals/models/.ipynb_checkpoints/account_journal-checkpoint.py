# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    category_id = fields.Many2one('approval.category', string="Category", required=False)

   
