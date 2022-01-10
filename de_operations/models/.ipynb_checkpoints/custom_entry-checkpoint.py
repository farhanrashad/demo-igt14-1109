# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    allow_advance_inv = fields.Boolean(string='Allow Advance')
    dp_product_id = fields.Many2one('product.product', string='Down Payment Product', domain=[('type', '=', 'service')],)
    
class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    allow_advance_inv = fields.Boolean(related='custom_entry_type_id.allow_advance_inv')
    
    #bill_count = fields.Integer(compute="_compute_all_bills", string='Bill Count', copy=False, default=0,)
    
    #@api.depends('move_id')
    def _compute_all_moves(self):
        Move = self.env['account.move']
        can_read = Move.check_access_rights('read', raise_exception=False)
        for move in self:
            move.invoice_count = can_read and Move.search_count([('custom_entry_id', '=', move.id),('move_type', '!=', 'entry'),('journal_id', '=', move.custom_entry_type_id.journal_id.id)]) or 0
            move.move_count = can_read and Move.search_count([('custom_entry_id', '=', move.id),('move_type', '=', 'entry'),('journal_id', '=', move.custom_entry_type_id.journal_id.id)]) or 0

    
    