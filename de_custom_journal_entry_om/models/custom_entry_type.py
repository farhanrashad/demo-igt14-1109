# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    has_om = fields.Selection(CATEGORY_SELECTION, string="Has OM Invoices", default="no", required=True,)
    allow_advance_inv = fields.Boolean(string='Allow Advance')
    dp_product_id = fields.Many2one('product.product', string='Down Payment Product', domain=[('type', '=', 'service')],)
    amount_advance_limit = fields.Float(string='Advance Amount Limit %')
    advance_journal_id = fields.Many2one('account.journal', string="Accounting Journal", company_dependent=True, check_company=True, domain="[('type', 'not in', ['bank', 'cash'])]")
    allow_om_deudction = fields.Boolean(string='Allow OM Deduction')
    auto_post_journal_entry = fields.Boolean(string='Auto Post Journal Entry')
    @api.constrains('amount_advance_limit')
    def _check_amount_advance_limit(self):
        if self.amount_advance_limit > 100 or self.amount_advance_limit <= 0.00:
            raise UserError(_('The limit of the down payment amount must be between 1 to 100.'))
            
class CustomEntryOMDeductionType(models.Model):
    _name = 'account.custom.entry.om.deduction.type'
    _description = 'Custom Entry OM Deduction Type'
    
    name = fields.Char(string='Name', required=True, translate=True)
    product_id = fields.Many2one('product.product', string="Product", ondelete='cascade')
    
