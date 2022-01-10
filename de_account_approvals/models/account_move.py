# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, date_utils, email_split, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from itertools import zip_longest
from hashlib import sha256
from json import dumps

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    category_id = fields.Many2one('approval.category', related='journal_id.category_id', string="Category", required=False)
    approval_state = fields.Selection([
        ('new', 'Draft'),
        ('pending', 'In Approval'),
        ('approved', 'Approved')
    ],default='new')
    
    approval_request_id = fields.Many2one('approval.request', string='Approval Request', copy=False, readonly=True)
    request_status = fields.Selection(related='approval_request_id.request_status')
    approvers_count = fields.Integer(compute='_compute_approvers_count')

    def _compute_approvers_count(self):
        Approvers = self.env['approval.approver']
        can_read = Approvers.check_access_rights('read', raise_exception=False)
        for subscription in self:
            subscription.approvers_count = can_read and Approvers.search_count([('move_id', '=', subscription.id)]) or 0
        
    def action_submit(self):
        approver_ids  = []
        request_list = []
        for move in self:
            request_list.append({
                'name': move.name,
                'request_owner_id': move.user_id.id,
                'category_id': move.category_id.id,
                'move_id': move.id,
                'reason': move.user_id.name + ' Has requested ' + move.name + ' for approval.' ,
                'request_status': 'new',
            })
            if self.name == 'draft' or self.name == 'Draft' or self.name == '/':
                self.name = move._get_move_display_name()
            approval_request_id = self.env['approval.request'].sudo().create(request_list)
            approval_request_id._onchange_category_id()
            approval_request_id.action_confirm()
            move.approval_request_id = approval_request_id.id
        self.approval_state = 'pending'
