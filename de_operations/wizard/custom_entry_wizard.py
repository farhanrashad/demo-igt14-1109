# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CustomEntryWizard(models.TransientModel):
    _name = "account.custom.entry.wizard.inv"
    _description = "Custom Entry Wizard"
        
    product_id = fields.Many2one('product.product', string='Down Payment Product', domain=[('type', '=', 'service')],)
    amount = fields.Float('Down Payment Amount', digits='Account', default=1.0, help="The percentage of amount to be Billed in advance, taxes excluded.")
    amount_bal = fields.Float('Balance Amount', digits='Account', default=1.0, readonly=True)
    amount_advance = fields.Float('Advance Amount', digits='Account', compute='_compute_advance_amount')
    currency_id = fields.Many2one('res.currency', string='Currency')
    supplier_taxes_id = fields.Many2many("account.tax", string="Vendor Taxes", help="Taxes used for deposits")
    
    @api.model
    def default_get(self,  default_fields):
        res = super(CustomEntryWizard, self).default_get(default_fields)
        entry_id = self.env['account.custom.entry'].browse(self._context.get('active_ids',[]))
        
        res.update({
            'amount_bal': entry_id.amount_total,
            'currency_id': entry_id.currency_id.id,
            'product_id': entry_id.custom_entry_type_id.dp_product_id.id,
            #'supplier_taxes_id': entry_id.custom_entry_type_id.dp_product_id.supplier_taxes_id.ids,
            #'supplier_taxes_id': [(6, 0, entry_id.custom_entry_type_id.dp_product_id.supplier_taxes_id.ids)],
        })
        return res
    
    def create_invoices(self):
        if self.amount > 100 or self.amount <= 0.00:
            raise UserError(_('The value of the down payment amount must be between 1 to 100.'))
            
        entry_id = self.env['account.custom.entry'].browse(self._context.get('active_ids', []))
        invoice = self.env['account.move']
        lines_data = []
        amount = (self.amount / 100) * entry_id.amount_total
        lines_data.append([0,0,{
            'name': _('Down Payment'),
            'price_unit': amount or 0.0,
            'quantity': 1.0,
            'product_uom_id': self.product_id.uom_id.id,
            'product_id': self.product_id.id,
            #'tax_ids': [(6, 0, tax_ids.ids)],
            #'analytic_account_id': line.analytic_account_id.id,
            #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
            #'project_id': line.project_id.id,
        }])
        invoice.create({
            'move_type': entry_id.custom_entry_type_id.move_type,
            'custom_entry_id': entry_id.id,
            'invoice_date': fields.Datetime.now(),
            'partner_id': entry_id.partner_id.id,
            #'partner_shipping_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'journal_id': entry_id.custom_entry_type_id.journal_id.id,
            'invoice_origin': entry_id.name,
            #'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': entry_id.partner_id.property_supplier_payment_term_id.id,
            'narration': entry_id.name,
            'invoice_user_id': entry_id.user_id.id,
            #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
            'invoice_line_ids':lines_data,
        })
        return invoice
    
    def _create_invoice(self, order, po_line, amount):
        if self.amount > 100 or self.amount <= 0.00:
            raise UserError(_('The value of the down payment amount must be between 1 to 100.'))
        #invoice_vals = self._prepare_bill_values(order, name, amount, po_line)
    
    @api.depends('amount')
    def _compute_advance_amount(self):
        for wizard in self:
            wizard.amount_advance = wizard.amount_bal * (wizard.amount / 100)
    