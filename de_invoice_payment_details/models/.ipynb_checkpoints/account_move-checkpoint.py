# -*- coding: utf-8 -*-

import json
from odoo import models
from odoo.tools.safe_eval import safe_eval

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    payment_ids = fields.Char(string='Payments')
    invoice_payment_ids = fields.Many2many('account.payment',  string='Payments', compute='_compute_payments')
    
    def _compute_payments(self):
        invoice_payments_widget = json.loads(self.invoice_payments_widget)
        payment_ids = []
        if invoice_payments_widget:
            for item in invoice_payments_widget["content"]:
                payment_ids.append(item["account_payment_id"])
        #for payment in payment_ids:
        self.invoice_payment_ids = payment_ids
        
