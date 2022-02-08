# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'    
    
    reconcile_amount = fields.Float(string='Reconcile Amount', compute='_compute_reconcile_amount')
    debit_allocation_ids = fields.One2many('account.payment.debit.allocation', 'payment_id', string='Debit Lines', copy=False) 
    credit_allocation_ids = fields.One2many('account.payment.credit.allocation', 'payment_id', string='Credit Lines', copy=False) 
    
    #payment_move_id = fields.Many2one('account.move', string='Entry')
    #payment_move_line_ids = fields.Many2many('account.move.line', string='Journal Items', domain="[('move_id','=',payment_move_id)]", compute='_compute_move_lines')

    writeoff_account_id = fields.Many2one('account.account', string='Writeoff Account')
    writeoff_label = fields.Char(string='Label', default='Write-Off')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    
    debit_total_currency = fields.Monetary(string='Debit Total', compute='_total_all_currency', currency_field='currency_id')
    credit_total_currency = fields.Monetary(string='Credit Total', compute='_total_all_currency', currency_field='currency_id')
    diff_amount_currency = fields.Monetary(string='Difference', compute='_total_all_currency')
    
    debit_total = fields.Monetary(string='Debit Total', default=1, compute='_total_all', currency_field='company_currency_id')
    credit_total = fields.Monetary(string='Credit Total', compute='_total_all', currency_field='company_currency_id')
    diff_amount = fields.Monetary(string='Difference', compute='_total_all', currency_field='company_currency_id')
    
    exchange_rate = fields.Char(string='Exchange Rate', compute='_compute_all_exchange')
    last_exchange_rate = fields.Char(string='Last Exchange Rate', readonly="1", compute='_compute_all_exchange')
    
    reconciled = fields.Boolean(string='Reconciled',copy=False)
    
    matching_move_id = fields.Many2one('account.move', string='Matching Entry', copy=False)
    matching_move_line_ids = fields.Many2many('account.move.line', string='Journal Items', domain="[('move_id','=',matching_move_id)]", compute='_compute_move_lines')

    def _compute_move_lines(self):
        if self.matching_move_id:
            for move in self.matching_move_id:
                self.matching_move_line_ids = move.line_ids + self.move_id.line_ids
        else:
            self.matching_move_line_ids = False
                    
    def action_generate_journal_entry(self):
        for payment in self:
            if not payment.writeoff_account_id:
                if payment.diff_amount_currency != 0:
                    raise UserError(_("Cannot create unbalanced journal entry. \nDifferences debit - credit: %s") % (str(payment.diff_amount_currency)))
                
            debit_sum = credit_sum = 0.0
            amount = 0
            total_debit_diff = total_credit_diff = 0
            line_ids = update_line_ids = []
            exchange_diff_currency = 0
            temp = ''
            #if payment.move_id:
            #    if payment.move_id == 'draft':
            #        payment.move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id).unlink()
                    #payment.payment_move_id.unlink()
            if payment.matching_move_id:
                if payment.matching_move_id.state == 'posted':
                    payment.matching_move_id.button_draft()
                    payment.matching_move_id.button_cancel()
                else:
                    payment.matching_move_id.unlink()
                    
            if not (payment.currency_id.id == payment.company_id.currency_id.id):
                #amount = payment.currency_id._get_conversion_rate(payment.currency_id, payment.company_id.currency_id,payment.company_id, fields.date.today()) * payment.amount
                amount = payment.currency_id._convert(payment.amount, payment.company_id.currency_id, payment.company_id, fields.date.today())                    

            else:
                amount = payment.amount
            journal_id = self.env['account.journal'].search([('type','=','general')],limit=1)
            move_dict = {
                'journal_id': journal_id.id, #self.journal_id.id,
                'date': self.date,
                'state': 'draft',
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'payment_id': payment.id,
            }
            payment_display_name = {
                'outbound-customer': _("Customer Reimbursement"),
                'inbound-customer': _("Customer Payment"),
                'outbound-supplier': _("Vendor Payment"),
                'inbound-supplier': _("Vendor Reimbursement"),
            }
            default_line_name = self.env['account.move.line']._get_default_line_name(_("Internal Transfer") if self.is_internal_transfer else payment_display_name['%s-%s' % (self.payment_type, self.partner_type)], self.amount, self.currency_id, self.date, partner=self.partner_id,)
            # --------------------------------------------
            # Greate move lines for incoming payment
            # --------------------------------------------
            if payment.payment_type == 'inbound':
                #generate cash/bank line for outgoing payment - credit line
                line_ids.append([0,0,{
                    'name': payment.ref or default_line_name,
                    'ref': payment.name,
                    #'move_line_id': payment_entry.id, 
                    'debit': round(payment.amount_total_signed,2),
                    'credit': 0.0,
                    #'account_id': payment.journal_id.payment_debit_account_id.id,
                    'account_id': payment.destination_account_id.id,
                    'payment_id': payment.id,
                    'currency_id': payment.currency_id.id,
                    'amount_currency':  payment.amount,
                    'partner_id': payment.partner_id.id,
                    'matched_payment_id': payment.id,
                    'payment_id': payment.id,
                }])
                temp += 'payment==' + str(round(payment.amount_total_signed,2)) + ' credit=' + str(0) + ' amount currency=' + str(round(payment.amount,2)) + '\n'

            # --------------------------------------------
            # Greate move lines for outgoing payment
            # --------------------------------------------
            if payment.payment_type == 'outbound':
                #generate cash/bank line for outgoing payment - credit line
                line_ids.append([0,0,{
                    'name': payment.ref or default_line_name,
                    'ref': payment.name,
                    #'move_line_id': payment_entry.id, 
                    'debit': 0.0,
                    'credit': round(payment.amount_total_signed,2),
                    #'account_id': payment.journal_id.payment_credit_account_id.id,
                    'account_id': payment.destination_account_id.id,
                    'payment_id': payment.id,
                    'currency_id': payment.currency_id.id,
                    'amount_currency':  payment.amount * -1,
                    'partner_id': payment.partner_id.id,
                    'matched_payment_id': payment.id,
                    'payment_id': payment.id,
                }])
            # --------------------------------------------
            # generate contra credit lines for selected debit allocation lines
            # --------------------------------------------
            for line in payment.debit_allocation_ids:
                if line.is_allocate:
                    line_ids.append([0,0,{
                        'name': line.move_line_id.name,
                        #'move_line_id': payment_entry.id,
                        'ref': line.move_line_id.move_id.name,
                        'debit': 0.0,
                        'credit': round(abs(line.allocated_amount),2),
                        'account_id': line.account_id.id,
                        'payment_id': payment.id,
                        'currency_id': payment.currency_id.id,
                        'amount_currency':  line.allocated_amount_currency * -1,
                        'payment_id': payment.id,
                        'allocation_move_line_id': line.move_line_id.id,
                        'partner_id': payment.partner_id.id,
                    }])
                    temp += 'Allocation=' + str(0) + ' credit=' + str(round(abs(line.allocated_amount),2)) + ' amount currency=' + str(round(line.allocated_amount_currency * -1,2)) + '\n'
            # --------------------------------------------
            # generate contra debit lines for selected credit allocation lines
            # --------------------------------------------
            for line in payment.credit_allocation_ids:
                if line.is_allocate:
                    line_ids.append([0,0,{
                        'name': line.move_line_id.name,
                        'ref': line.move_line_id.move_id.name,
                        #'move_line_id': payment_entry.id,
                        'debit': round(abs(line.allocated_amount),2),
                        'credit': 0.0,
                        'account_id': line.account_id.id,
                        'payment_id': payment.id,
                        'currency_id': payment.currency_id.id,
                        'amount_currency':  line.allocated_amount_currency,
                        'payment_id': payment.id,
                        'allocation_move_line_id': line.move_line_id.id,
                        'partner_id': payment.partner_id.id,
                    }])    
            # --------------------------------------------
            # Post Difference Entry
            # --------------------------------------------
            if payment.diff_amount > 0:
                total_debit_diff = payment.diff_amount
                total_credit_diff = 0
            elif payment.diff_amount < 0:
                total_debit_diff = 0
                total_credit_diff = payment.diff_amount
                
            if payment.writeoff_account_id:
                line_ids.append([0,0,{
                    'name': payment.writeoff_label,
                    'ref': payment.name,
                    #'move_line_id': payment_entry.id,
                    'debit': round(abs(total_debit_diff),2),
                    'credit': round(abs(total_credit_diff),2),
                    'account_id': payment.writeoff_account_id.id,
                    'payment_id': payment.id,
                    'currency_id': payment.currency_id.id,
                    #'amount_currency': round(payment.diff_amount_currency,2),
                    'payment_id': payment.id,
                    'partner_id': payment.partner_id.id,
                }])
                temp += 'writeoff/debit=' + str(round(abs(total_debit_diff),2)) + ' credit=' + str(round(abs(total_credit_diff),2)) + ' amount currency=' + str(round(payment.diff_amount_currency,2)) + '\n'
            #raise ValidationError(_(temp))
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            payment.matching_move_id = move.id
            payment.matching_move_id._post(soft=False)
            #payment.move_id.write(move_dict)
            #payment.payment_move_id=move.id
            #payment.move_id = move.id
    
    def action_post(self):
        ''' draft -> posted '''
        self.move_id._post(soft=False)
        self.action_generate_journal_entry()
        self.action_reconcile()
        
        
    
    def action_reconcile(self):
        for payment in self:
            if payment.credit_allocation_ids or payment.debit_allocation_ids:
                payment_line = self.move_id.line_ids.filtered(lambda line: line.account_id.id == payment.destination_account_id.id) 
                #sorted_lines = payment_line
                #involved_lines = debit_line = credit_line = payment_line
                debit_lines = credit_lines = payment_line
                #sorted_lines = self.env['account.move.line']
                
                domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False)]
                if payment.payment_type == 'outbound':
                    debit_lines += payment.move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id)
                    credit_lines += payment.matching_move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id and line.matched_payment_id.id == payment.id)
                elif payment.payment_type == 'inbound':
                    credit_lines += payment.move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id)
                    debit_lines += payment.matching_move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id and line.matched_payment_id.id == payment.id)
                #debit_lines += payment.debit_allocation_ids.filtered(lambda line: line.is_allocate == True).move_line_id.filtered_domain(domain)
                #credit_lines = payment.credit_allocation_ids.filtered(lambda line: line.is_allocate == True).move_line_id.filtered_domain(domain)
                for account in payment.move_id.line_ids.account_id.filtered(lambda x: x.internal_type in ['receivable','payable']):
                            (debit_lines + credit_lines)\
                                .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
                                .reconcile()
                
                # --------------------------------------------
                # Reconcile entries for outoing payment
                # --------------------------------------------
                if self.payment_type == 'outbound' or self.payment_type == 'inbound':
                    #sorted_lines = self.sorted(key=lambda line: (line.date_maturity or line.date, line.currency_id))
                    for line in self.debit_allocation_ids.filtered(lambda line: line.is_allocate == True):
                        debit_line = line.move_line_id
                        credit_line = self.env['account.move.line'].search([('allocation_move_line_id','=',line.move_line_id.id),('move_id','=',payment.matching_move_id.id)])
                        (credit_line + debit_line)\
                            .filtered_domain([('account_id', '=', line.account_id.id), ('reconciled', '=', False)])\
                            .reconcile()
                    for line in self.credit_allocation_ids.filtered(lambda line: line.is_allocate == True):
                        credit_line = line.move_line_id
                        debit_line = self.env['account.move.line'].search([('allocation_move_line_id','=',line.move_line_id.id),('move_id','=',payment.matching_move_id.id)])
                        (debit_line + credit_line)\
                            .filtered_domain([('account_id', '=', line.account_id.id), ('reconciled', '=', False)])\
                            .reconcile()
                    for account in payment.move_id.line_ids.account_id.filtered(lambda x: x.internal_type in ['receivable','payable']):
                            (debit_lines + credit_lines)\
                                .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
                                .reconcile()
                        
                    #for line in self.debit_allocation_ids:
                    #    if line.is_allocate == True:
                    #        payment_line += self.env['account.move.line'].search([('id','=',line.move_line_id.id)])
                    #for line in self.credit_allocation_ids:
                    #    if line.is_allocate == True:
                    #        sorted_lines += self.env['account.move.line'].search([('id','=',line.move_line_id.id)])
                    #    involved_lines = sorted_lines + payment_line
                    #    payment_lines = self.move_id.line_ids.filtered_domain(domain)
                    #    payment_lines += payment.debit_allocation_ids.move_line_id.filtered_domain(domain)
                    #    #for account in payment_lines.account_id:
                    #    for account in payment.destination_account_id:    
                    #        (payment_lines + sorted_lines)\
                    #            .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
                    #            .reconcile()
            payment.update({
                'is_reconciled': True,
                #'reconciled': True
            })
                    
    @api.depends('debit_allocation_ids.allocated_amount', 'credit_allocation_ids.allocated_amount','amount','payment_type')
    def _total_all_currency(self):
        debit_total = 0.0
        credit_total = 0.0   
        for payment in self:    
            for dr_line in payment.debit_allocation_ids:
                if dr_line.is_allocate == True:
                    debit_total += dr_line.allocated_amount_currency
            for cr_line in payment.credit_allocation_ids:
                if cr_line.is_allocate == True:
                    credit_total += cr_line.allocated_amount_currency
            if payment.payment_type == 'inbound':
                credit_total += payment.amount
            if payment.payment_type == 'outbound':
                debit_total += payment.amount    
            payment.update({
                'debit_total_currency': debit_total,
                'credit_total_currency': credit_total,
                'diff_amount_currency': (debit_total - credit_total),
            })
    
    #@api.depends('debit_allocation_ids.allocated_amount', 'credit_allocation_ids.allocated_amount','amount_total_signed','payment_type')
    def _total_all(self):
        debit_total = 0.0
        credit_total = 0.0
        writeoff_amt = 0.0
        diff_amt = 0.0
        for payment in self:
            debit_total = sum(payment.debit_allocation_ids.filtered(lambda line: line.is_allocate == True).mapped('allocated_amount'))
            credit_total = sum(payment.credit_allocation_ids.filtered(lambda line: line.is_allocate == True).mapped('allocated_amount'))
            if payment.payment_type == 'inbound':
                credit_total += payment.amount_total_signed
            #elif payment.payment_type == 'outbound':
            else:
                debit_total += payment.amount_total_signed
            
            diff_amt = (debit_total - credit_total)
            
            if payment.writeoff_account_id:
                writeoff_amt = abs(debit_total - credit_total)
                #if diff_amt > 0:
                #    diff_amt -= writeoff_amt
                #else:
                #    diff_amt += writeoff_amt
            payment.update({
                'debit_total': debit_total,
                'credit_total': credit_total,
                'diff_amount': diff_amt,
            })
            
    
    def _compute_reconcile_amount(self):
        for payment in self:
            reconcile_amount = 0.0
            for move_line in payment.move_id.line_ids:
                for credit_line in move_line.matched_credit_ids:
                    reconcile_amount = reconcile_amount + credit_line.amount
                for debit_line in move_line.matched_debit_ids:
                    reconcile_amount = reconcile_amount + debit_line.amount        
            payment.update({
                'reconcile_amount' : reconcile_amount
            })
        #    if payment.reconciled_invoices_count > 0:
        #        if payment.reconcile_amount == payment.amount:
        #            payment.update({
        #                'is_reconciled' : True
        #            })
        #    else:
        #        payment.update({
        #            'is_reconciled': False
        #        })
                   

    def action_process_openitems(self):
        debit_lines = []
        credit_lines = []
        residual_amount = residual_amount_currency = 0
        self.debit_allocation_ids.unlink()
        self.credit_allocation_ids.unlink()
        debit_move_lines = self.env['account.move.line'].search([('partner_id','=',self.partner_id.id),('debit','!=',0),('move_id.state','=','posted'),('account_id.reconcile','=',True),('amount_residual_currency','!=',0),('move_id','!=',self.move_id.id),('payment_id','=',False)])
        for debit_line in debit_move_lines:                
            if not (debit_line.currency_id.id == self.currency_id.id):
                #residual_amount_currency = debit_line.currency_id._get_conversion_rate(debit_line.currency_id, self.currency_id,self.company_id, fields.date.today()) * debit_line.amount_residual_currency
                residual_amount_currency = debit_line.currency_id._convert(debit_line.residual_amount_currency, self.company_id.currency_id, self.company_id, fields.date.today())                    

            else:
                residual_amount_currency = debit_line.amount_residual_currency
                
            debit_lines.append((0,0,{
                'move_id': debit_line.move_id.id,
                'account_id': debit_line.account_id.id,  
                'move_line_id': debit_line.id,
                'date': debit_line.move_id.invoice_date,
                'due_date': debit_line.move_id.invoice_date_due,
                'invoice_amount': debit_line.amount_currency,
                'unallocated_amount': debit_line.amount_residual,
                'unallocated_amount_currency': residual_amount_currency,
                'is_allocate': False,
                'allocated_amount': debit_line.amount_residual,
                'allocated_amount_currency': residual_amount_currency,
                 'currency_id': debit_line.move_id.currency_id.id,
                 'company_currency_id': self.company_id.currency_id.id, 
                'allocation_currency_id': self.currency_id.id,
            }))
        self.debit_allocation_ids  =  debit_lines
        
        #Generate Credit Lines
        residual_amount_currency = 0.0
        credit_move_lines = self.env['account.move.line'].search([('partner_id','=',self.partner_id.id),('debit','=',0),('move_id.state','=','posted'),('account_id.reconcile','=',True),('amount_residual_currency','!=',0),('payment_id','=',False)])
        for credit_line in credit_move_lines:
                
            if not (credit_line.currency_id.id == self.currency_id.id):
                #residual_amount_currency = credit_line.currency_id._get_conversion_rate(credit_line.currency_id, self.currency_id,self.company_id, fields.date.today()) * credit_line.amount_residual_currency
                residual_amount_currency = credit_line.currency_id._convert(credit_line.residual_amount_currency, self.company_id.currency_id, self.company_id, fields.date.today())                    

            else:
                residual_amount_currency = credit_line.amount_residual_currency
                
            credit_lines.append((0,0,{
                        'move_id': credit_line.move_id.id,
                        'account_id': credit_line.account_id.id,  
                        'move_line_id': credit_line.id,
                        'date': credit_line.move_id.invoice_date,
                        'due_date': credit_line.move_id.invoice_date_due,
                        'invoice_amount': abs(credit_line.amount_currency),
                        'unallocated_amount': abs(credit_line.amount_residual),
                        'unallocated_amount_currency': abs(residual_amount_currency),
                        'is_allocate': False,
                        'allocated_amount_currency': abs(residual_amount_currency),
                 'allocated_amount': abs(credit_line.amount_residual),
                        'currency_id': credit_line.move_id.currency_id.id,
                        'company_currency_id': self.company_id.currency_id.id, 
                        'allocation_currency_id': self.currency_id.id,
            }))
        self.credit_allocation_ids  =  credit_lines   
        
    
    
    def action_exchange_rate(self, currency, exchange_amount):
        line_src_ids = []
        exchange_journal = self.env['account.journal'].search([('name','=','Exchange Difference')], limit=1)
        if not exchange_journal :
            journal_vals = {
                            'name': 'Exchange Difference',
                            'code': 'EXCH',
                            'company_id': self.env.company,
                        }
            exchange_journal = self.env['account.journal'].create(journal_vals)
        procuretags = self.env['account.analytic.tag'].search([('name','=','Procurement & Vendor Management')], limit=1)
        if not procuretags:
            procure_tag = {
                    'name': 'Procurement & Vendor Management',
                }
            procuretags = self.env['account.analytic.tag'].create(procure_tag) 

            line_src_ids.append((0,0, {
                    'account_id':  self.payment_id.destination_account_id.id,
                    'partner_id':  self.payment_id.partner_id.id,
                    'name': 'Currency exchange rate difference',
                    'amount_currency': exchange_amount,
                     'currency_id':  currency,
                    'analytic_tag_ids': [(6, 0, procuretags.ids)],
                    }))
                        
        ext_account = self.env['account.account'].search([('name' ,'=', 'Foreign Exchange Gain')], limit=1)
        if not ext_account:
            account_vals = {
                        'name': 'Foreign Exchange Gain',
                        'code': 441000,
                        'user_type_id': 13 ,
            }
            ext_account = self.env['account.account'].create(account_vals)
        line_src_ids.append ((0,0, {
                    'account_id':  ext_account.id,
                    'partner_id':  self.payment_id.partner_id.id,
                    'name': 'Currency exchange rate difference',
                    'amount_currency': exchange_amount,
                    'currency_id':  currency,
                    'analytic_tag_ids': [(6, 0, procuretags.ids)],
        }))
 
        move_values = {
                    'date': fields.date.today(),
                    'move_type': 'entry',
                    'invoice_date': fields.date.today(),
                    'journal_id': exchange_journal.id,
                    'currency_id': self.payment_id.currency_id.id, 
                    'line_ids': line_src_ids,
            }
        exchange_moves = self.env['account.move'].create(move_values) 
        return exchange_moves

    def _compute_all_exchange(self):
        exchange_rate = 0
        if not self.currency_id.id == self.company_currency_id.id:
            #exchange_rate = self.currency_id._get_conversion_rate(self.currency_id, self.company_currency_id,self.company_id, fields.date.today()) * 1
            exchange_rate = self.currency_id._convert(1, self.company_id.currency_id, self.company_id, fields.date.today())                    

            self.exchange_rate = '1 ' + str(self.company_currency_id.name) + ' = ' + str(round(exchange_rate,2)) + ' ' + str(self.currency_id.name)
            self.last_exchange_rate = 'At the operation date, the exchange rate was 1 ' + str(self.company_currency_id.name) + ' = ' + str(round(exchange_rate,2)) + ' ' + str(self.currency_id.name)
        else:
            self.exchange_rate = '1 ' + str(self.company_currency_id.name) + ' = ' + '1' + ' ' + str(self.currency_id.name)
            self.last_exchange_rate = '1 ' + str(self.company_currency_id.name) + ' = ' + '1' + ' ' + str(self.currency_id.name)

class AccountPaymentDebitAllocation(models.TransientModel):
    _name = 'account.payment.debit.allocation'
    _description = 'Payment debit Allocation'
    _order = 'is_allocate desc, date desc'

    move_id = fields.Many2one('account.move', string='Invoice', store=True)
    payment_id = fields.Many2one('account.payment', 'Payment', help="Change to a better name", index=True)
    move_line_id = fields.Many2one('account.move.line', string='Line Id')
    account_id = fields.Many2one('account.account', string='Account', store=True)
    date = fields.Date(string='Date', store=True)
    due_date = fields.Date(string='Due Date', store=True)
    invoice_amount = fields.Monetary(string='Invoice Amount', store=True, currency_field='currency_id')
    unallocated_amount = fields.Monetary(string='Unallocated Amount', store=True, currency_field='company_currency_id')
    unallocated_amount_currency = fields.Monetary(string='Unallocated Curr.', store=True, currency_field='allocation_currency_id')
    is_allocate = fields.Boolean(string='Allocate', store=True)
    allocated_amount_currency = fields.Monetary(string='Allocate Curr.', store=True, currency_field='allocation_currency_id')
    allocated_amount = fields.Monetary(string='Allocate Amount', store=True, readonly="1", currency_field='company_currency_id', compute="_compute_all_currency_amount" )
    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=False,
        string='Currency')
    allocation_currency_id = fields.Many2one('res.currency', related='payment_id.currency_id')
    company_currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=False,
        string='Invoice Currency')

    
    @api.depends('allocated_amount_currency')
    def _compute_all_currency_amount(self):
        total_allocation = 0.0
        for record in self:
            #total_allocation = record.allocation_currency_id._get_conversion_rate(record.allocation_currency_id, record.company_currency_id,record.payment_id.company_id, fields.date.today()) * float(record.allocated_amount_currency)
            total_allocation = record.currency_id._convert(record.allocated_amount_currency, self.company_id.currency_id, self.company_id, fields.date.today())                    

            record.allocated_amount = float(total_allocation)
        
    @api.onchange('allocated_amount_currency')
    def onchange_allocated_amount(self):
        for line in self:
            if line.allocated_amount_currency > line.unallocated_amount_currency:
                raise UserError('Allocated amount cannot be greater than! '+str(line.unallocated_amount_currency))
                
class AccountPaymentCreditAllocation(models.TransientModel):
    _name = 'account.payment.credit.allocation'
    _description = 'Payment Credit Allocation'
    _order = 'is_allocate desc, date desc'

    move_id = fields.Many2one('account.move', string='Invoice', store=True)
    payment_id = fields.Many2one('account.payment', 'Payment', help="Change to a better name", index=True)
    move_line_id = fields.Many2one('account.move.line', string='Line Id')
    account_id = fields.Many2one('account.account', string='Account', store=True)
    date = fields.Date(string='Date', store=True)
    due_date = fields.Date(string='Due Date', store=True)
    invoice_amount = fields.Monetary(string='Invoice Amount', store=True, currency_field='currency_id')
    unallocated_amount = fields.Monetary(string='Unallocated Amount', store=True, currency_field='company_currency_id')
    unallocated_amount_currency = fields.Monetary(string='Unallocated Curr.', store=True, currency_field='allocation_currency_id')
    is_allocate = fields.Boolean(string='Allocate', store=True)
    
    allocated_amount_currency = fields.Monetary(string='Allocate Curr.', store=True, currency_field='allocation_currency_id')
    allocated_amount = fields.Monetary(string='Allocate Amount', store=True, readonly="1", currency_field='company_currency_id', compute="_compute_all_currency_amount" )
    
    exchange_diff = fields.Monetary(string='Exchange Diff.', store=True, readonly="1", currency_field='company_currency_id', compute="_compute_all_exchange" )

        
    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=False,
        string='Currency')
    allocation_currency_id = fields.Many2one('res.currency', related='payment_id.currency_id')
    company_currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=False,
        string='Invoice Currency')
        
    @api.depends('allocated_amount_currency')
    def _compute_all_currency_amount(self):
        total_allocation = 0.0
        for record in self:
            #total_allocation = record.allocation_currency_id._get_conversion_rate(record.allocation_currency_id, record.company_currency_id,record.payment_id.company_id, fields.date.today()) * float(record.allocated_amount_currency)
            total_allocation = record.currency_id._convert(record.allocated_amount_currency, self.company_id.currency_id, self.company_id, fields.date.today())                    

            record.allocated_amount = float(total_allocation)
        
    @api.onchange('allocated_amount_currency')
    def onchange_allocated_amount(self):
        for line in self:
            if line.allocated_amount_currency > line.unallocated_amount_currency:
                raise UserError('Allocated amount cannot be greater than! '+str(line.unallocated_amount_currency))
                
    def _compute_all_exchange(self):
        for line in self:
            current_exchange = 0
            last_exchange = 0
            if not line.currency_id.id == line.allocation_currency_id.id:
                #last_exchange = line.allocation_currency_id._get_conversion_rate(line.allocation_currency_id, line.company_currency_id,line.payment_id.company_id, line.date) * 1
                last_exchange = line.currency_id._convert(1, self.company_id.currency_id, self.company_id, fields.date.today())                    

                #current_exchange = line.allocation_currency_id._get_conversion_rate(line.allocation_currency_id, line.company_currency_id,line.payment_id.company_id, fields.date.today()) * 1
                #current_exchange = line.company_currency_id._get_conversion_rate(line.company_currency_id, line.allocation_currency_id,line.payment_id.company_id, fields.date.today()) * 1
                current_exchange = line.currency_id._convert(1, self.company_id.currency_id, self.company_id, fields.date.today())                    

            line.exchange_diff = current_exchange
