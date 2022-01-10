# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    account_period = fields.Char(string='Period', compute='_compute_account_period')
    
    @api.depends('date')
    def _compute_account_period(self):
        for record in self:
            record.account_period = record.date.strftime("%m/%Y")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    account_period = fields.Char(related='move_id.account_period')
    
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    account_period = fields.Char(string='Period', compute='_compute_account_period')
    
    @api.depends('date')
    def _compute_account_period(self):
        for record in self:
            record.account_period = record.date.strftime("%m/%Y")