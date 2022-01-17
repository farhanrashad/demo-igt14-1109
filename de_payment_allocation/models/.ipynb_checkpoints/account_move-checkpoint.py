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

import ast
import json
import re
import warnings


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    reconcile_amount = fields.Float(string='Reconcile Amount', compute='_compute_reconcile_amount')
    
    
    def _compute_reconcile_amount(self):
        for entry in self:
            reconcile_amount = 0.0
            for move_line in entry.line_ids:
                for credit_line in move_line.matched_credit_ids:
                    reconcile_amount = reconcile_amount + credit_line.amount
                for debit_line in move_line.matched_debit_ids:
                    reconcile_amount = reconcile_amount + debit_line.amount        
            entry.update({
                'reconcile_amount' : reconcile_amount
            })
            
    
     
    
class AccountMoveLine(models.Model):
    _inherit= 'account.move.line'
    
    allocation_move_line_id = fields.Many2one('account.move.line', string='Move Line')
    reconcile_amount = fields.Float(string='Reconcile Amount',  compute='_compute_reconcile_amount')
    is_reconciled = fields.Boolean(string='Is Reconcile', store=True)
    matched_payment_id = fields.Many2one('account.payment', string='Matched Payment', copy=False)
    
    
    def _compute_reconcile_amount(self):
        for line in self:
            reconcile_amount = 0.0
            for move_line in self:
                for credit_line in move_line.matched_credit_ids:
                    reconcile_amount = reconcile_amount + credit_line.amount
                for debit_line in move_line.matched_debit_ids:
                    reconcile_amount = reconcile_amount + debit_line.amount        
            line.update({
                'reconcile_amount' : reconcile_amount
            })
            if line.debit > 0:
                if line.reconcile_amount == line.debit:
                    line.update({
                        'is_reconciled' : True
                    })
            elif line.credit > 0:
                if line.reconcile_amount == line.credit:
                    line.update({
                        'is_reconciled' : True
                    })        
            else:
                line.update({
                    'is_reconciled': False
                })

    
class AccountMove(models.Model):
    _inherit = 'decimal.precision'    

    