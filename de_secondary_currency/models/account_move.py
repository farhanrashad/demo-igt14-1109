# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from itertools import groupby
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class AccountMove(models.Model):
    _inherit = "account.move"
    
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    total_base_signed = fields.Monetary(string='Total base.Curr.', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    
    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_all_currency_conversion_amount(self):
        for move in self:
            total_base_signed = 0.0
            if not (move.currency_id.id == move.company_id.currency_id.id):
                #total_base_signed += move.currency_id._get_conversion_rate(move.currency_id, move.company_currency_id,move.company_id, move.date) * move.amount_total_signed
                total_base_signed = move.currency_id._convert(move.amount_total_signed, move.company_id.currency_id, move.company_id, fields.date.today()) 

            else:
                total_base_signed = move.amount_total_signed
            move.update({
                'total_base_signed': total_base_signed,
            })