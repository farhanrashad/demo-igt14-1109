# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

class HrExpenseSheetType(models.Model):
    _name = 'hr.expense.sheet.type'
    _description = 'Expense Sheet Type'
    
    name = fields.Char(string='Expense Type', required=True, translate=True)
    group_id = fields.Many2one('res.groups', string='Security Group')
    journal_id = fields.Many2one('account.journal', string='Journal', )
    move_type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], string='Type', default="entry")
    
class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    sheet_ref = fields.Char(string='Reference', readonly=True, default=lambda self: 'HEX/')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Line Manager Approval'),
        ('approve', 'Expense Category Approval'),
        ('exp_approve', 'Finance Approval'),
        ('fin_approve', 'Waiting Account Entries'),
        ('post', 'Waiting Payment'),
        ('payment', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    
    
    hr_salary_advance_id  = fields.Many2one('hr.salary.advance', string='Advances Request', domain='[("employee_id","=", employee_id), ("state","in", ("paid","close"))]')
    
    hr_expense_sheet_type_id  = fields.Many2one('hr.expense.sheet.type', string='Expense Type')
    
    total_currency_amount = fields.Float(string='Total curr.Amount', compute='_compute_curr_amount', store=True, tracking=True)
    
    total_approved_amount = fields.Monetary('Approved Amount', currency_field='currency_id', compute='_compute_approved_amount', store=True, tracking=True)
    
    @api.depends('expense_line_ids.total_amount')
    def _compute_curr_amount(self):
        for sheet in self:
            sheet.total_currency_amount = sum(sheet.expense_line_ids.mapped('total_amount'))
    
    @api.depends('expense_line_ids.amount_approved')
    def _compute_approved_amount(self):
        for sheet in self:
            sheet.total_approved_amount = sum(sheet.expense_line_ids.mapped('amount_approved'))
            
    @api.model
    def create(self, vals):
        vals['sheet_ref'] = self.env['ir.sequence'].get('hr.expense.sheet') or ' '
        sheet = super(HrExpenseSheet, self.with_context(mail_create_nosubscribe=True, mail_auto_subscribe_no_notify=True)).create(vals)
        sheet.activity_update()
        return sheet
    
    # --------------------------------------------
    # Expense Sheet Submit Button
    # --------------------------------------------
    def action_submit_sheet(self):
        for sheet in self.sudo():
            group_id = sheet.hr_expense_sheet_type_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to submit request in category '%s'.", sheet.hr_expense_sheet_type_id.name))
            
            if not sheet.expense_line_ids:
                raise UserError(_("You cannot submit expense '%s' because there is no line.", self.name))
                
            if not sheet.total_amount:
                raise UserError(_("You cannot submit expense '%s' with 0 amount.", self.name))
                    
        self.write({'state': 'submit'})
        self.activity_update()
    
    # --------------------------------------------
    # Expense Sheet Approval Buttons
    # --------------------------------------------
    def approve_expense_finance(self):
        #Finanace Approval
        #for line in self.expense_line_ids:
        #    if line.expense_approved:
        #        if line.total_amount != line.amount_approved and line.fin_remarks == False:
        #            raise UserError(_("Approved amount is different than advance amount, Please specify remarks"))
        #            break
                    
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('There are no expense reports to approve.'),
                'type': 'warning',
                'sticky': False,  #True/False will display for few seconds if false
            },
        }
        
        #Line Finance Approval
        filtered_sheet_exp = self.filtered(lambda s: s.state in ['exp_approve'])
        if not filtered_sheet_exp:
            return notification
        for sheet in filtered_sheet_exp:
            sheet.write({'state': 'fin_approve', 'user_id': sheet.user_id.id or self.env.user.id})
        
        notification['params'].update({
            'title': _('The expense reports were successfully approved.'),
            'type': 'success',
            'next': {'type': 'ir.actions.act_window_close'},
        })
        
    def approve_expense_category(self):
        for line in self.expense_line_ids:
        #    if line.expense_approved:
        #        if line.total_amount != line.amount_approved and line.remarks == False:
        #            raise UserError(_("Approved amount is different than advance amount, Please specify remarks"))
        #            break
            expense_type_id = self.env['hr.expense.type'].search([('id','=',line.expense_type_id.id)],limit=1)
            group_id = expense_type_id.group_id
            if group_id:
                if (group_id & self.env.user.groups_id):
                    if line.expense_approved == True or line.remarks != False:
                        line.write({
                            'state': 'approved', 
                        })
        
        #Line Category Expense Approval
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('There are no expense reports to approve.'),
                'type': 'warning',
                'sticky': False,  #True/False will display for few seconds if false
            },
        }
        
        if all(expense.state == 'approved' for expense in self.expense_line_ids.filtered(lambda p: p.sheet_id.state == 'approve')):
            filtered_sheet_apr = self.filtered(lambda s: s.state in ['approve'])
            if not filtered_sheet_apr:
                return notification
            for sheet in filtered_sheet_apr:
                sheet.write({'state': 'exp_approve', 'user_id': sheet.user_id.id or self.env.user.id})
        
            notification['params'].update({
                'title': _('The expense reports were successfully approved.'),
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            })
                            
    def approve_expense_sheets(self):
        expense_type_id = self.env['hr.expense.type']
        if not self.user_has_groups('hr_expense.group_hr_expense_team_approver'):
            raise UserError(_("Only Managers and HR Officers can approve expenses"))
        elif not self.user_has_groups('hr_expense.group_hr_expense_manager'):
            current_managers = self.employee_id.expense_manager_id | self.employee_id.parent_id.user_id | self.employee_id.department_id.manager_id.user_id

            if self.employee_id.user_id == self.env.user:
                raise UserError(_("You cannot approve your own expenses"))

            if not self.env.user in current_managers and not self.user_has_groups('hr_expense.group_hr_expense_user') and self.employee_id.expense_manager_id != self.env.user:
                raise UserError(_("You can only approve your department expenses"))
                
        #for line in self.expense_line_ids:
        #    if line.expense_approved:
        #        if line.total_amount != line.amount_approved and line.remarks == False:
        #            raise UserError(_("Approved amount is different than advance amount, Please specify remarks"))
        #            break
        #    else:
        #        line.update({
        #            'expense_approved': False,
        #        })
        
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('There are no expense reports to approve.'),
                'type': 'warning',
                'sticky': False,  #True/False will display for few seconds if false
            },
        }
        #Line Manager Approval
        if self.state in ('submit','draft'):
            filtered_sheet = self.filtered(lambda s: s.state in ['submit', 'draft'])
            if not filtered_sheet:
                return notification
            for sheet in filtered_sheet:
                sheet.write({'state': 'approve', 'user_id': sheet.user_id.id or self.env.user.id})
            
        notification['params'].update({
            'title': _('The expense reports were successfully approved.'),
            'type': 'success',
            'next': {'type': 'ir.actions.act_window_close'},
        })
    
    # --------------------------------------------
    # Action Create Journal Entry
    # --------------------------------------------
    def action_sheet_create_entry(self):
        move = self.env['account.move']
        company = self.company_id
        lines_data = []
        debit = credit = amount = balance = balance_currency = 0
        counter_debit = counter_credit = counter_amount = counter_balance = 0
        
        for sheet in self:
            debit = credit = amount = balance = balance_currency = 0
            
            if any(sheet.state != 'fin_approve' for sheet in self):
                raise UserError(_("You can only generate accounting entry for approved expense(s)."))

            if any(not sheet.journal_id for sheet in self):
                raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))
            
            expense_line_ids = self.mapped('expense_line_ids')\
            .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
            
            for expense in sheet.expense_line_ids:
                if not (expense.currency_id.id == expense.company_id.currency_id.id):
                    debit = expense.company_currency_id._convert(expense.amount_approved, expense.currency_id, expense.company_id, fields.date.today())                    
                else:
                    debit = expense.amount_approved
                
                debit = expense.company_currency_id._convert(expense.amount_approved, expense.currency_id, expense.company_id, fields.date.today())                    

                partner_id = expense.employee_id.sudo().address_home_id.commercial_partner_id.id
                
                account_src = expense._get_expense_account_source()
                ccount_dst = expense._get_expense_account_destination()
                lines_data.append([0,0,{
                    'name': str(expense.name) + ' ' ,
                    'account_id': account_src.id,
                    'amount_currency': expense.amount_approved,
                    'currency_id': sheet.currency_id.id,
                    'debit': expense.amount_approved_signed,
                    'credit': 0,
                    'partner_id': partner_id,
                    'quantity': expense.quantity,
                    'product_uom_id': expense.product_id.uom_id.id,
                    'product_id': expense.product_id.id,
                    'analytic_account_id': expense.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)],
                    'project_id': expense.project_id.id,
                    'expense_id': expense.id,
                    'date': fields.Datetime.now(),
                }])
                credit += expense.amount_approved_signed
                balance_currency += expense.amount_approved
            lines_data.append([0,0,{
                'name': str(self.name) + ' ' ,
                'account_id': sheet.employee_id.address_home_id.property_account_payable_id.id,
                'amount_currency': balance_currency * -1,
                'currency_id': sheet.currency_id.id,
                'debit': 0,
                'credit': credit,
                'partner_id': partner_id,
                'quantity': 1,
                'date': fields.Datetime.now(),
                #'product_uom_id': expense.product_id.uom_id.id,
                #'product_id': expense.product_id.id,
                #'analytic_account_id': expense.analytic_account_id.id,
                #'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)],
                #'project_id': expense.project_id.id,
                #'expense_id': expense.id,
            }])
            move = self.env['account.move'].create({
                'move_type': sheet.hr_expense_sheet_type_id.move_type,
                'ref':  str(sheet.sheet_ref), 
                'date': fields.Datetime.now(),
                'currency_id': sheet.currency_id.id,
                'journal_id': sheet.hr_expense_sheet_type_id.journal_id.id,
                'narration': sheet.name,
                'line_ids':lines_data,
            })
            sheet.update({
                'account_move_id': move.id,
                'journal_id': sheet.hr_expense_sheet_type_id.journal_id.id,
                'accounting_date': fields.Datetime.now(),
            })
            move._post()
            to_post = self.filtered(lambda sheet: sheet.payment_mode == 'own_account' and sheet.expense_line_ids)
            to_post.write({'state': 'post'})
            (self - to_post).write({'state': 'done'})
            self.activity_update()
            
            
    # --------------------------------------------
    # Actions
    # --------------------------------------------
    def action_sheet_move_create1(self):
        samples = self.mapped('expense_line_ids.sample')
        if samples.count(True):
            if samples.count(False):
                raise UserError(_("You can't mix sample expenses and regular ones"))
            self.write({'state': 'post'})
            return

        if any(sheet.state != 'fin_approve' for sheet in self):
            raise UserError(_("You can only generate accounting entry for approved expense(s)."))

        if any(not sheet.journal_id for sheet in self):
            raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

        expense_line_ids = self.mapped('expense_line_ids')\
            .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
        
        res = expense_line_ids.action_move_create()
        for sheet in self.filtered(lambda s: not s.accounting_date):
            sheet.accounting_date = sheet.account_move_id.date
        to_post = self.filtered(lambda sheet: sheet.payment_mode == 'own_account' and sheet.expense_line_ids)
        to_post.write({'state': 'post'})
        (self - to_post).write({'state': 'done'})
        self.activity_update()
        # change status of advances
        #expense.hr_salary_advance_id.hr_expense_sheet_id = self.id
        #for expense in expense_line_ids:
            #expense.hr_salary_advance_id.state = 'close'
            #expense.advance_line_id.state = 'close'
            #expense.hr_salary_advance_id.hr_expense_id = expense.id
            #expense.hr_salary_advance_id.hr_expense_id = expense.id
        return res
    
class HrExpenseType(models.Model):
    _name = 'hr.expense.type'
    _description = 'Expense Type'
    
    name = fields.Char(string='Expense Category', required=True, translate=True)
    group_id = fields.Many2one('res.groups', string='Security Group')

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    #hr_salary_advance_id  = fields.Many2one('hr.salary.advance', string='Advances Request', domain='[("employee_id","=", employee_id), ("state","in", ("paid","close"))]')

    hr_salary_advance_id  = fields.Many2one('hr.salary.advance', string='Advances Request', )
    advance_line_id  = fields.Many2one('hr.salary.advance.line', string='Advances Line', domain='[("advance_id","=", hr_salary_advance_id)]')
    project_id = fields.Many2one('project.project', string='Project')
    hr_expense_sheet_type_id  = fields.Many2one('hr.expense.sheet.type', related='sheet_id.hr_expense_sheet_type_id')
    expense_type_id = fields.Many2one('hr.expense.type', string='Expense Category', copy=False)
    
    amount_approved = fields.Monetary(string='Approved Amount', compute='_compute_amount_approved', store=True)
    expense_approved = fields.Boolean(string='Is Approved', default=True)
    remarks = fields.Char(string='Remarks')
    fin_remarks = fields.Char(string='Finance Remarks')
    company_currency_id = fields.Many2one(string='Company Currency', readonly=True, related='company_id.currency_id')

    total_amount_company = fields.Monetary("Total (Company Currency)", compute='_compute_total_amount_company', store=True, currency_field='company_currency_id')
    
    amount_approved_signed = fields.Monetary("Approved Signed", compute='_compute_total_approved_company', currency_field='company_currency_id')


    """
    @api.depends('total_amount')
    def _compute_amount_approved(self):
        for line in self:
            line.update({
                'amount_approved': line.total_amount,
            })
    #@api.depends('product_id', 'company_id')
    def _compute_from_product_id_company_id(self):
        for expense in self.filtered('product_id'):
            expense = expense.with_company(expense.company_id)
            expense.name = expense.name or expense.product_id.display_name
            if not expense.attachment_number or (expense.attachment_number and not expense.unit_amount):
                expense.unit_amount = expense.unit_amount
            expense.product_uom_id = expense.product_id.uom_id
            expense.tax_ids = expense.product_id.supplier_taxes_id.filtered(lambda tax: tax.company_id == expense.company_id)  # taxes only from the same company
            account = expense.product_id.product_tmpl_id._get_product_accounts()['expense']
            if account:
                expense.account_id = account
    
   """
    # --------------------------------------------
    # calculate amount in company currency
    # --------------------------------------------
    def _compute_total_approved_company(self):
        for expense in self:
            amount = 0
            if expense.company_currency_id:
                date_expense = expense.date
                amount = expense.currency_id._convert(
                    expense.amount_approved, expense.company_id.currency_id,
                    expense.company_id, date_expense or fields.Date.today())
            expense.amount_approved_signed = amount
            
    @api.depends('date', 'total_amount', 'company_currency_id','amount_approved')
    def _compute_total_amount_company(self):
        for expense in self:
            amount = 0
            if expense.company_currency_id:
                date_expense = expense.date
                amount = expense.company_currency_id._convert(
                    expense.amount_approved, expense.currency_id,
                    expense.company_id, date_expense or fields.Date.today())
            expense.total_amount_company = amount
            
    # --------------------------------------------
    # Prepare Journal Entry
    # --------------------------------------------
    def _prepare_move_values(self):
        """
        This function prepares move values related to an expense
        """
        self.ensure_one()
        journal = self.sheet_id.bank_journal_id if self.payment_mode == 'company_account' else self.sheet_id.journal_id
        account_date = self.sheet_id.accounting_date or self.date
        move_values = {
            'journal_id': journal.id,
            'move_type': self.sheet_id.hr_expense_sheet_type_id.move_type,
            'company_id': self.sheet_id.company_id.id,
            'date': account_date,
            'ref': self.sheet_id.name,
            'currency_id': self.sheet_id.currency_id.id,
            # force the name to the default value, to avoid an eventual 'default_name' in the context
            # to set it to '' which cause no number to be given to the account.move when posted.
            'name': '/',
        }
        return move_values
    
    # --------------------------------------------
    # Prepare Journal Entry Lines
    # --------------------------------------------
    def _get_account_move_line_values(self):
        move_line_values_by_expense = {}
        for expense in self:
            move_line_name = expense.employee_id.name + ': ' + expense.name.split('\n')[0][:64]
            account_src = expense._get_expense_account_source()
            account_dst = expense._get_expense_account_destination()
            account_date = expense.sheet_id.accounting_date or expense.date or fields.Date.context_today(expense)

            company_currency = expense.company_id.currency_id

            move_line_values = []
            taxes = expense.tax_ids.with_context(round=True).compute_all(expense.amount_approved, expense.currency_id, 1, expense.product_id)
            total_amount = 0.0
            total_amount_currency = 0.0
            partner_id = expense.employee_id.sudo().address_home_id.commercial_partner_id.id

            # source move line
            balance = expense.currency_id._convert(taxes['total_excluded'], company_currency, expense.company_id, account_date)
            #balance = expense.amount_approved
            amount_currency = taxes['total_excluded']
            move_line_src = {
                'name': move_line_name,
                'quantity': expense.quantity or 1,
                'debit': balance if balance > 0 else 0,
                'credit': -balance if balance < 0 else 0,
                'amount_currency': amount_currency,
                'account_id': account_src.id,
                'product_id': expense.product_id.id,
                'product_uom_id': expense.product_id.uom_id.id,
                'analytic_account_id': expense.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)],
                'expense_id': expense.id,
                'partner_id': partner_id,
                'tax_ids': [(6, 0, expense.tax_ids.ids)],
                'tax_tag_ids': [(6, 0, taxes['base_tags'])],
                'currency_id': expense.currency_id.id,
            }
            move_line_values.append(move_line_src)
            total_amount -= balance
            total_amount_currency -= move_line_src['amount_currency']

            # taxes move lines
            for tax in taxes['taxes']:
                balance = expense.currency_id._convert(tax['amount'], company_currency, expense.company_id, account_date)
                amount_currency = tax['amount']

                if tax['tax_repartition_line_id']:
                    rep_ln = self.env['account.tax.repartition.line'].browse(tax['tax_repartition_line_id'])
                    base_amount = self.env['account.move']._get_base_amount_to_display(tax['base'], rep_ln)
                    base_amount = expense.currency_id._convert(base_amount, company_currency, expense.company_id, account_date)
                else:
                    base_amount = None

                move_line_tax_values = {
                    'name': tax['name'],
                    'quantity': 1,
                    'debit': balance if balance > 0 else 0,
                    'credit': -balance if balance < 0 else 0,
                    'amount_currency': amount_currency,
                    'account_id': tax['account_id'] or move_line_src['account_id'],
                    'tax_repartition_line_id': tax['tax_repartition_line_id'],
                    'tax_tag_ids': tax['tag_ids'],
                    'tax_base_amount': base_amount,
                    'expense_id': expense.id,
                    'partner_id': partner_id,
                    'currency_id': expense.currency_id.id,
                    'analytic_account_id': expense.analytic_account_id.id if tax['analytic'] else False,
                    'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)] if tax['analytic'] else False,
                }
                total_amount -= balance
                total_amount_currency -= move_line_tax_values['amount_currency']
                move_line_values.append(move_line_tax_values)

            # destination move line
            move_line_dst = {
                'name': move_line_name,
                'debit': total_amount > 0 and total_amount,
                'credit': total_amount < 0 and -total_amount,
                'account_id': account_dst,
                'date_maturity': account_date,
                'amount_currency': total_amount_currency,
                'currency_id': expense.currency_id.id,
                'expense_id': expense.id,
                'partner_id': partner_id,
            }
            move_line_values.append(move_line_dst)

            move_line_values_by_expense[expense.id] = move_line_values
        return move_line_values_by_expense
    
    @api.onchange('hr_salary_advance_id')
    def onchange_advaces(self):
        if self.hr_salary_advance_id:
            self.update({
                #'name': self.hr_salary_advance_id.name, 
                #'product_id': self.hr_salary_advance_id.product_id.id,
                #'unit_amount': self.hr_salary_advance_id.amount_total,
                #'currency_id': self.hr_salary_advance_id.currency_id,
                'quantity': 1,
                'payment_mode': 'own_account',
            })
            
    @api.onchange('advance_line_id')
    def onchange_advace_line(self):
        if self.advance_line_id:
            self.update({
                #'unit_amount': self.advance_line_id.unit_price,
                'quantity': self.advance_line_id.quantity,
                'product_id': False,
            })
    
    @api.onchange('total_amount')
    def onchange_total_amount(self):
        if self.total_amount:
            self.update({
                'amount_approved': self.total_amount,
            })