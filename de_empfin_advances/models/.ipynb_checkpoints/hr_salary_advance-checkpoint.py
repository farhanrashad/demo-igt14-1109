# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class SalaryAdvancePayment(models.Model):
    _name = "hr.salary.advance"
    _description = 'Salary Advance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    def _default_get_contract(self):
        contract_id = self.env['hr.contract'].search([('employee_id','=', self.employee_id.id),('state','=','open')], limit=1)        
        if contract_id:
            self.employee_contract_id = contract_id.id
        else:
            self.employee_contract_id = None       

    name = fields.Char(string='Name', readonly=True, default=lambda self: 'Adv/')
    #employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_id = fields.Many2one('hr.employee', compute='_compute_employee_id', string="Employee",
        store=True, required=True, readonly=False, tracking=True,
        states={'approved': [('readonly', True)], 'done': [('readonly', True)]},
        default=_default_employee_id, check_company=True)
    
    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.today())
    reason = fields.Text(string='Reason')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    exceed_condition = fields.Boolean(string='Exceed than maximum',
                                      help="The Advance is greater than the maximum percentage in salary structure")
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', readonly=True,)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Waiting Line Manager Approval'),
                              ('hr_approval', 'Waiting HR Approval'),
                              ('finance_approval', 'Waiting Finance Approval'),
                              ('accepted', 'Waiting Accounting Entries'),
                              ('approved', 'Waiting Payment'),
                              ('paid', 'Open'),
                              ('close', 'Close'),
                              ('cancel', 'Cancelled'),
                              ('reject', 'Rejected')], string='Status', default='draft', compute='_compute_state', store=True)
    employee_contract_id = fields.Many2one('hr.contract', string='Contract', default=_default_get_contract, domain="[('employee_id','=',employee_id),('state','=','open')]")
        
    deductable = fields.Boolean(string='Deductable', default=False)
    allow_rolling = fields.Boolean(string='Rolling', default=False)
    partner_id = fields.Many2one('res.partner', 'Employee Partner', readonly=False, states={'paid': [('readonly', True)]},)
    journal_id = fields.Many2one('account.journal', string='Journal', )
    journal_type = fields.Selection(related='journal_id.type', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True, compute='_get_payment')
    invoice_id = fields.Many2one('account.move', string='Bill', readonly=True, compute='_get_invoice')
    payment_date = fields.Date(string='Payment Date', compute='_compute_payment_date')

    payment_amount = fields.Monetary(string='Payment Amount', compute='_compute_payment_amount')
    #account_id = fields.Many2one('account.account',string="Account")
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type')
    bill_count = fields.Integer(string='Advances Bill', compute='get_bill_count')
    payment_count = fields.Integer(string='Payment Count', compute='get_payment_count')
    
    cash_line_ids = fields.One2many('hr.salary.advance.line', 'advance_id', string='Advances Line')
    amount_total = fields.Monetary(string='Approved Amount', store=True, readonly=True, compute='_amount_all')
    
    #expense details
    hr_expense_sheet_id = fields.Many2one('hr.expense.sheet', string='Expense Sheet', compute='_compute_expense_id')
    hr_expense_id = fields.Many2one('hr.expense', string='Expense', compute='_compute_expense_id')
    date_due_expense = fields.Datetime(string='Due On', compute='_compute_expense_deadline', )
    expense_deadline = fields.Datetime(string='Expense Deadline', compute='_compute_expense_deadline', )
    
    remittance_outstanding_days = fields.Integer(string='Remittance Outstanding day(s)', compute='_compute_remittance_days')
    remittance_overdue_days = fields.Integer(string='Remittance Overdue day(s)', compute='_compute_remittance_days')

    api.depends('company_id')
    def _compute_employee_id(self):
        if not self.env.context.get('default_employee_id'):
            for adv in self:
                adv.employee_id = self.env.user.with_company(adv.company_id).employee_id
    
    @api.depends('cash_line_ids.state')
    def _compute_state(self):
        status = ''
        for adv in self:
            #state = adv.mapped('cash_line_ids.state')
            #if state:
            if adv.cash_line_ids:
                for line in adv.cash_line_ids:
                    if line.state == 'close':
                        status = 'close'
                    else:
                        status = adv.state
                        break
            else:
                status = 'draft'
                #if state.count('close'):
                 #   status = 'close'
                #elif state.count('draft'):
                 #   status = 'draft'
                #else:
                 #   status = adv.state
            #else:
                #status = adv.state
            adv.state = status
            
    def _compute_remittance_days(self):
        date = expense_date = self.date
        for request in self:
            if request.state != 'close':
                date = fields.Date.from_string(request.date)
                request.remittance_outstanding_days = (fields.date.today() - date).days
                if request.hr_expense_id:
                    expense_date = request.hr_expense_id.date
                    request.remittance_overdue_days = (fields.date.today() - expense_date).days
                else:
                   request.remittance_overdue_days = 0 
            else:
                request.remittance_outstanding_days = 0
                request.remittance_overdue_days = 0
            
    @api.depends('date')    
    def _compute_expense_deadline(self):  
        dt = False
        days = 0
        for request in self:
            days = 30
            dt = fields.Date.to_string(request.date + timedelta(days))
            request.expense_deadline = dt
            request.date_due_expense = dt

    
    def _compute_expense_id(self):
        expense_ids = self.env['hr.expense'].search([('hr_salary_advance_id','=',self.id)])
        sheet_ids = self.env['hr.expense.sheet'].search([('hr_salary_advance_id','=',self.id)])
        if expense_ids:
            for expense_id in expense_ids:
                self.hr_expense_id = expense_id.id
        else:
            self.hr_expense_id = False
        if sheet_ids:
            for sheet_id in sheet_ids:
                self.hr_expense_sheet_id = sheet_id.id
        else:
            self.hr_expense_sheet_id = False
    
    def _compute_payment_amount(self):
        for request in self:
            invoice = self.env['account.move'].search([('hr_salary_advance_id','=',request.id)],limit=1)
            payment = self.env['account.payment'].search([('hr_salary_advance_id','=',request.id)],limit=1)
            if request.journal_type == 'purchase':
                request.payment_amount = invoice.amount_total
            else:
                request.payment_amount = payment.amount
                
    def get_bill_count(self):
        count = self.env['account.move'].search_count([('hr_salary_advance_id', '=', self.id),('journal_id.type', '=', 'purchase')])
        self.bill_count = count
        
    def get_payment_count(self):
        count = self.env['account.payment'].search_count([('hr_salary_advance_id', '=', self.id)])
        self.payment_count = count
      
    @api.depends('state')
    def _get_payment(self):
        payment_id = self.env['account.payment'].search([('hr_salary_advance_id','=',self.id)],limit=1)
        self.payment_id = payment_id.id
        if not payment_id:
            self.payment_id = False
            
    @api.depends('state')
    def _get_invoice(self):
        invoice = self.env['account.move'].search([('hr_salary_advance_id','=',self.id)],limit=1)
        self.invoice_id = invoice.id
        if not invoice:
            self.invoice_id = False
            
    def _compute_payment_date(self):
        for request in self:
            if request.journal_type == 'purchase':
                request.payment_date = request.invoice_id.invoice_date
            elif request.journal_type != 'purchase':
                request.payment_date = request.payment_id.date
            else:
                request.payment_date = False

    @api.onchange('employee_id')
    def _onchange_employee(self):
        self.partner_id = self.employee_id.address_home_id.id
        
    def unlink(self):
        if any(self.filtered(lambda loan: loan.state not in ('draft', 'cancel'))):
            raise UserError(_('You cannot delete a Loan which is not draft or cancelled!'))
        return super(SalaryAdvancePayment, self).unlink()
    
    #@api.onchange('employee_id')
    def onchange_employee_id(self, employee_id,employee_contract_id):
        if employee_id:
            employee_obj = self.env['hr.employee'].browse(employee_id)
            department_id = employee_obj.department_id.id
            employee_contract_id = employee_obj.contract_id.id
            domain = [('employee_id', '=', employee_id)]
            return {'value': {'department': department_id,'employee_contract_id':employee_contract_id}, 'domain': {'employee_contract_id': domain, }}

    @api.onchange('company_id')
    def onchange_company_id(self):
        company = self.company_id
        domain = [('company_id.id', '=', company.id)]
        result = {
            'domain': {
                'journal': domain,
            },

        }
        return result

    def submit_to_manager(self):
        if not self.cash_line_ids:
                raise UserError(_("You cannot submit advance request '%s' because there is no  line.", self.name))
        self.state = 'confirmed'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'confirmed'
            })

    def cancel(self):
        self.state = 'cancel'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'cancel'
            })

    def action_line_manager_approve(self):
        self.state = 'hr_approval'
        for cash_line in self.cash_line_ids:
            if cash_line.approved:
            #    if cash_line.approved_amount != cash_line.total_amount:
            #        if cash_line.approved:
            #            if not cash_line.remarks:
            #                raise UserError(_("Remarks are required for '%s' .", cash_line.desc))
                cash_line.update({
                    'state': 'hr_approval'
                })
            else:
                cash_line.update({
                    'state': 'reject',
                    'approved_amount': 0,
                })
        
    def action_hr_manager_approve(self):
        self.state = 'finance_approval'
        for cash_line in self.cash_line_ids:
            #if cash_line.approved:
            #    if cash_line.approved_amount != cash_line.total_amount:
            #        if cash_line.approved:
            #            if not cash_line.remarks:
            #                raise UserError(_("Remarks are required for '%s' .", cash_line.desc))
                            
            if cash_line.approved:
                cash_line.update({
                    'state': 'finance_approval'
                })
            else:
                cash_line.update({
                    'state': 'reject',
                    'approved_amount': 0,
                })
        
    def action_finance_manager_approve(self):
        self.state = 'accepted'
        for cash_line in self.cash_line_ids:
            #if cash_line.approved:
            #    if cash_line.approved_amount != cash_line.total_amount:
            #        if cash_line.approved:
            #            if not cash_line.finance_remarks:
            #                raise UserError(_("Remarks are required for '%s' .", cash_line.desc))
                            
            if cash_line.approved:
                cash_line.update({
                    'state': 'accepted'
                })
            else:
                cash_line.update({
                    'state': 'reject',
                    'approved_amount': 0,
                })
        
        
    def action_close(self):
        self.state = 'close'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'close'
            })
          
        
    def action_refuse(self):
        self.state = 'reject'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'reject'
            })

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Advances Bill',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
    
    def action_view_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Payment',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
        }
    
    @api.model
    def create(self, vals):
            
        vals['name'] = self.env['ir.sequence'].get('hr.salary.advance') or ' '
        res_id = super(SalaryAdvancePayment, self).create(vals)
        return res_id
    
    def action_payment(self):
        invoice = False
        #if self.account_id:
            #account_id = self.account_id.id
        #else:
            #account_id = False
            
        if self.journal_id.type == 'purchase':
            invoice = self.env['account.move']
            lines_data = []
            for line in self.cash_line_ids:
                #if self.account_id:
                    #account_id = self.account_id
                #else:
                    #account_id = False
                if line.approved:
                    lines_data.append([0,0,{
                        'product_id': line.product_id.id,
                        'name': line.desc,
                        'price_unit': line.approved_amount,
                        #'account_id': account_id,
                        'hr_salary_advance_line_id': line.id,
                        'quantity': 1,
                    }])
            invoice.create({
                'partner_id': self.partner_id.id,
                'move_type': 'in_invoice',
                'ref': self.name,
                #'origin': self.name,
                'invoice_date':self.date,
                'journal_id':self.journal_id.id,
                'hr_salary_advance_id':self.id,
                'currency_id': self.currency_id.id,
                'invoice_line_ids':lines_data,
            })
            invoice._post()
        
        elif self.journal_id.type in ('bank','cash'):
            payment = self.env['account.payment']
            payment.create({
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'partner_id': self.partner_id.id,
                'payment_method_id': self.payment_method_id.id,
                'company_id': self.company_id.id,
                'amount': self.amount_total,
                'currency_id': self.currency_id.id,
                'journal_id': self.journal_id.id,
                'date': fields.Date.today(),
                'ref': self.name,
                'hr_salary_advance_id':self.id,
            })
        self.update({
            'state': 'approved'
        })
        for cash_line in self.cash_line_ids:
            if cash_line.approved:
                cash_line.update({
                    'state': 'approved'
                })
        return invoice
    
    @api.depends('cash_line_ids.approved_amount')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.cash_line_ids:
                amount_untaxed += line.approved_amount
            order.update({
                'amount_total': amount_untaxed 
            })
    
    
class AdvancePayment(models.Model):
    _name = "hr.salary.advance.line"
    _description = 'Salary Advance Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='name'
    
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    type_id = fields.Many2one('hr.advance.type', string='Type')
    #product_id = fields.Many2one('product.product', string='Product', domain="[('can_be_expensed','=', True)]", required=True, change_default=True)
    product_id = fields.Many2one('product.product', string='Product', domain=[('type', '=', 'service')], change_default=True)
    desc = fields.Char(string='Description', oldname='description')
    quantity = fields.Float(string='Qunatity', required=1, default=1.0)
    unit_price = fields.Float(string='Unit Price', required=True, default=1.0)
    total_amount = fields.Monetary(compute='_compute_amount', string='Subtotal')
    currency_id = fields.Many2one(related='advance_id.currency_id', store=True, string='Currency', readonly=True)

    remarks = fields.Text(string='Remarks')
    finance_remarks = fields.Text(string='Finance Remarks')
    #approve_amount = fields.Float(string='Amount For Approval')
    approved_amount = fields.Monetary(string='Approved Amt', compute='_compute_approved_amount', store=True)
    advance_id = fields.Many2one('hr.salary.advance', string='Advances')
    employee_id = fields.Many2one(related='advance_id.employee_id')
    approved = fields.Boolean(string='Approved', default=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Waiting Line Manager Approval'),
                              ('hr_approval', 'Waiting HR Approval'),
                              ('finance_approval', 'Waiting Finance Approval'),
                              ('accepted', 'Waiting Accounting Entries'),
                              ('approved', 'Waiting Payment'),
                              ('paid', 'Open'),
                              ('close', 'Close'),
                              ('cancel', 'Cancelled'),
                              ('reject', 'Rejected')], string='Status', default='draft')
    
    #@api.constrains('approved_amount')
    #def _check_approved_amount(self):
        #for line in self:
            #if line.approved_amount > line.total_amount:
                #raise UserError(_('The amount is exceeded than requested amount'))
    
    def unlink(self):
        for adv in self:
            if adv.state != 'draft':
                raise UserError(_('You cannot delete a posted or approved advance.'))
        return super(AdvancePayment, self).unlink()
    
    @api.depends('type_id','advance_id')
    def _compute_name(self):
        for line in self:
            line.name = str(line.advance_id.name) + ' - ' + str(line.product_id.name)
            
    @api.onchange('type_id')
    def _onchange_type(self):
        for line in self:
            line.product_id = line.type_id.product_id.id
            #line.description = line.product_id.name
        
    @api.depends('total_amount','unit_price','quantity')
    def _compute_approved_amount(self):
        for line in self:
            line.update({
                'approved_amount': line.unit_price * line.quantity,
            })
            
    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.update({
                'total_amount': line.unit_price * line.quantity,
                #'approved_amount': line.unit_price * line.quantity,
            })
