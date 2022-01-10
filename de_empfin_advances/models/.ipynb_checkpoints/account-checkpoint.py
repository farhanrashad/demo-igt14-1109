# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    hr_salary_advance_id = fields.Many2one('hr.salary.advance', string='Salary Advance')
    
    def action_reconcile1(self):
        for payment in self:
            expense_id = self.env['hr.expense']
            advance_line_id = self.env['hr.salary.advance.line']
            #if payment.payment_move_id.state == 'draft':
            #payment.payment_move_id.sudo().action_post()
            if  self.credit_allocation_ids or self.debit_allocation_ids:
                #Outbound Reconcilliation
                #payment_debit_line =  payment_credit_line = reconcile_amount = reconcile_amount_currency = 0 
                payment_line = self.payment_move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id)
                
                sorted_lines = payment_line
                involved_lines = debit_line = credit_line = payment_line
                debit_lines = credit_lines = payment_line
                sorted_lines = self.env['account.move.line']
                
                domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False),('move_id', '=', payment.payment_move_id.id)]
                debit_lines += payment.payment_move_id.line_ids.filtered(lambda line: line.account_id.id == self.destination_account_id.id)
                debit_lines += payment.debit_allocation_ids.move_line_id.filtered_domain(domain)
                credit_lines = payment.credit_allocation_ids.move_line_id.filtered_domain(domain)
                
                # --------------------------------------------
                # Reconcile entries for outoing payment
                # --------------------------------------------
                if self.payment_type == 'outbound' or self.payment_type == 'inbound':
                    #sorted_lines = self.sorted(key=lambda line: (line.date_maturity or line.date, line.currency_id))
                    for line in self.debit_allocation_ids.filtered(lambda line: line.is_allocate == True):
                        debit_line = line.move_line_id
                        credit_line = self.env['account.move.line'].search([('allocation_move_line_id','=',line.move_line_id.id),('move_id','=',payment.payment_move_id.id)])
                        (credit_line + debit_line)\
                            .filtered_domain([('account_id', '=', line.account_id.id), ('reconciled', '=', False)])\
                            .reconcile()
                        advance_line_id = self.env['hr.salary.advance.line'].search([('id','=',line.move_line_id.hr_salary_advance_line_id.id)])
                        #advance_line_id["state"] = 'draft'
                        advance_line_id.sudo().update({
                            #'desc': 'test11',
                            #'quantity': 1,
                            'state': 'close'
                        })
                    
                    for line in self.credit_allocation_ids.filtered(lambda line: line.is_allocate == True):
                        credit_line = line.move_line_id
                        debit_line = self.env['account.move.line'].search([('allocation_move_line_id','=',line.move_line_id.id),('move_id','=',payment.payment_move_id.id)])
                        (debit_line + credit_line)\
                            .filtered_domain([('account_id', '=', line.account_id.id), ('reconciled', '=', False)])\
                            .reconcile()
                    for account in payment.move_id.line_ids.account_id.filtered(lambda x: x.internal_type in ['receivable','payable']):    
                            (debit_lines + credit_lines)\
                                .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
                                .reconcile()
            payment.update({
                'is_reconciled': True,
                'reconciled': True
            })
            
                
            
    def action_reconcile2(self):
        #res = super(AccountPayment, self).action_reconcile()
        temp = ''
        #self.sudo().action_reconcile()
        expense_id = self.env['hr.expense']
        advance_line_id = self.env['hr.salary.advance.line']
        if self.debit_allocation_ids.filtered(lambda x: x.is_allocate == True):
            for line in self.debit_allocation_ids.filtered(lambda x: x.is_allocate == True).move_line_id:
                advance_line_id = self.env['hr.salary.advance.line'].search([('id','=',line.hr_salary_advance_line_id.id)])
                #advance_line_id["state"] = 'draft'
                advance_line_id.sudo().update({
                    #'desc': 'test11',
                    #'quantity': 1,
                    'state': 'close'
                })
                
                temp += 'advance=' + str(advance_line_id.name) + '-' + str(advance_line_id.advance_id.name) + ' | '
                expense_id = self.env['hr.expense'].search([('advance_line_id','=',advance_line_id.id)],limit=1)
                #expense_id["is_editable"] = True
                #expense_id.sudo().update({
                #    'state': 'done'
                #})
                temp += 'expense=' + str(expense_id.sheet_id.sheet_ref) + '-' + str(expense_id.name) + '\n'
                #self.env.cr.execute(""" UPDATE hr_salary_advance_line SET state = 'close' WHERE id = %s ;""" % (advance_line_id.id, ))
            #res = super(AccountPayment, self).action_reconcile()
            #raise UserError(_(temp))
        #return super(AccountPayment, self).action_reconcile()
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    hr_salary_advance_id = fields.Many2one('hr.salary.advance', string='Salary Advance')
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    hr_salary_advance_line_id = fields.Many2one('hr.salary.advance.line', string='Salary Advance Line')


