# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime

class PurchaseSubscriptionAdjustments(models.TransientModel):
    _name = 'purchase.subscription.adjust.entry.wizard'
    _description = 'Purchase Subscription Adjustments'
    
    @api.model
    def default_get(self,  default_fields):
        res = super(PurchaseSubscriptionAdjustments, self).default_get(default_fields)
        subscription = self.env['purchase.subscription'].browse(self._context.get('active_ids',[]))
        order = []
        #for subscription in subscriptions:
        #    order.append((0,0,{
        #        'journal_id' : subscription.subscription_plan_id.journal_id.id,
        #    }))
        res.update({
            'journal_id': subscription.subscription_plan_id.journal_id.id,
            'purchase_subscription_id': subscription.id,
            })
        return res
    
    date = fields.Date('Date',default=datetime.today())
    invoice_type = fields.Selection([
        ('in_invoice', 'Bill'),
        ('in_refund', 'Credit Memo')
    ], string='Invoice Type', default='in_refund', required=True)
    product_id = fields.Many2one('product.product','Product',required=True, domain="[('purchase_subscription','=', True)]")
    adjustment_payment_method = fields.Selection([
        ('percentage', 'percentage'),
        ('fixed', 'fixed amount')
        ], string='Payment Method', default='fixed', required=True,)

    ref = fields.Char(string='Reference', copy=False, tracking=True)
    #amount = fields.Float('Amount', digits='Product Price', )
    amount = fields.Float('Adjustment Amount', digits='Account', help="The percentage of amount to be Billed in advance, taxes excluded.")
    #price_unit = fields.Float(string='Unit Price', digits='Product Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    fixed_amount = fields.Monetary('Amount (Fixed)', )
    purchase_subscription_id = fields.Many2one('purchase.subscription','Vendor Bill',)

    invoice_id = fields.Many2one('account.move','Vendor Bill', required=False, domain="[('journal_id.type', '=', 'purchase'),('purchase_subscription_id', '=', purchase_subscription_id)]",)
    invoiced_amount = fields.Float('Invoiced Amount', digits='Account', readonly=True,)
    
    journal_id = fields.Many2one('account.journal','Journal', required=True, domain="[('type','=','purchase')]")
    reason = fields.Text('Reason')
          
    #@api.model
    #def default_get(self, fields_list):
        # OVERRIDE
        #res = super().default_get(fields_list)
        
    #@api.onchange('adjustment_payment_method')
    #def onchange_adjustment_payment_method(self):
        #if self.adjustment_payment_method == 'percentage':
            #amount = self.default_get(['amount']).get('amount')
            #return {'value': {'amount': amount}}
        #return {}
    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        self.ref = self.invoice_id.name
        self.invoiced_amount = self.invoice_id.amount_total
        
    def create_invoices(self):
        subscriptions = self.env['purchase.subscription'].browse(self._context.get('active_ids', []))

        if self.invoice_type:
            for order in subscriptions:
                amount, name = self._get_advance_details(order)
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                #tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_id).ids
                analytic_tag_ids = []
                #for line in order.order_line:
                    #analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
                moves = self._create_invoice(order, amount)

        if self._context.get('open_bills', False):
            return subscriptions.action_subscription_invoice()
        return {'type': 'ir.actions.act_window_close'}
    
    def _get_advance_details(self, order):
        context = {'lang': order.partner_id.lang}
        if self.adjustment_payment_method == 'percentage':
            amount = order.recurring_total * self.amount / 100
            #name = _("Adjustments of %s%%") % (self.amount)
        else:
            amount = self.fixed_amount
        name = self.reason
        del context

        return amount, name
    
    def _create_invoice(self, order, amount):
        if (self.adjustment_payment_method == 'percentage' and self.amount <= 0.00) or (self.adjustment_payment_method == 'fixed' and self.fixed_amount <= 0.00):
            raise UserError(_('The value of the down payment amount must be positive.'))

        amount, name = self._get_advance_details(order)

        invoice_vals = self._prepare_bill_values(order, name, amount,)

        #if order.fiscal_position_id:
            #invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id
        invoice = self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
        invoice.message_post_with_view('mail.message_origin_link',
                    values={'self': invoice, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return invoice
    
    def _prepare_bill_values(self, order, name, amount,):
        partner_invoice_id = order.partner_id.address_get(['invoice'])['invoice']
        invoice_vals = {
            'ref': self.ref,
            'move_type': self.invoice_type,
            'narration': self.reason,
            'invoice_origin': order.name,
            'purchase_subscription_id': order.id,
            'invoice_user_id': order.user_id.id,
            'partner_id': partner_invoice_id,
            #'fiscal_position_id': (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(order.partner_id.id)).id,
            'currency_id': order.currency_id.id,
            'payment_reference': self.ref or '',
            'invoice_payment_term_id': order.payment_term_id.id,
            'partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': self.product_id.uom_id.id,
                'purchase_subscription_id': order.id,
                #'tax_ids': [(6, 0, po_line.taxes_id.ids)],
                'analytic_tag_ids': [(6, 0, order.analytic_tag_ids.ids)],
                'analytic_account_id': order.analytic_account_id.id or False,
            })],
        }

        return invoice_vals
