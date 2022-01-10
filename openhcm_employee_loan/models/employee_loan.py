from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from datetime import datetime
from dateutil.relativedelta import relativedelta

   
class employee_loanForm(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='employee.loan'
    _description="Employee Loan"
#     _rec_name='code'
    
    
    def action_view_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
#             'multi': False,
            'name': 'Installment',
            'domain': [('order_line','=', self.id)],
            'target': 'current',
            'res_model': 'employee.loan.installment',
            'view_mode': 'tree,form',
        }
    

 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit Request'),
        ('h_r','HR Approval'),
        ('dept_approve','Finance Approval'),
        ('refuse','Rejected'),
        ('done', 'Done'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    
    def unlink(self):
        for leave in self:
            if leave.state in ('done','h_r','dept_approve'):
                raise UserError(_('You cannot delete an order form  which is not draft or cancelled. '))
     
            return super(employee_loanForm, self).unlink()
    
    @api.constrains('loan_amount')    
    def onchange_loanamount(self):
        for s in self:
            if s.loan_amount<=0 or s.loan_amount<=0.00:
                raise Warning("You can't add less than zero amount Loan!") 
    
    def draft(self):
        self.write({'state':'submit'}) 

    def submit(self):
        self.write({'state':'h_r'}) 
           
    def h_r(self):
        self.write({'state':'done'})
     
    @api.onchange('interest_rate','loan_amount')   
    def interest_convert(self):
        for s in self:
            s.interest_amount=(s.interest_rate/100)*s.loan_amount 
        
        
    def compute_sheet(self):
        for s in self:
            
            if s.interest_amount and s.loan_amount and s.term:
                if s.term:
                    line=[(5,0,0)]
                    z=0
                    k=0
                    for ss in range(self.term):
                        z=z+1
                        k=k+1
                        date_after_month = self.start_date+ relativedelta(months=k)
                        vals = {
                                    'name':self.name+'-'+str(z),
                                    'date':date_after_month,
                                    'loan_amount':self.loan_amount,
                                    'interest':self.interest_amount/self.term,
                                    'total_interest':self.interest_amount,
                                    'installment_amount':self.loan_amount/self.term,
                                    'total':(self.loan_amount/self.term)+(self.interest_amount/self.term)
                                }
                        
                        
                        line.append((0, 0, vals))
                            
                            
                    self.statements_line=line
                    
            elif s.loan_amount and s.term:
                if s.term:
                    line=[(5,0,0)]
                    z=0
                    k=0
                    for ss in range(self.term):
                        z=z+1
                        k=k+1
                        date_after_month = self.start_date+ relativedelta(months=k)
                        vals = {
                                    'name':self.name+'-'+str(z),
                                    'date':date_after_month,
                                    'loan_amount':self.loan_amount,
                                    'interest':0.0,
                                    'total_interest':0.0,
                                    'installment_amount':self.loan_amount/self.term,
                                    'total':(self.loan_amount/self.term)+(self.interest_amount/self.term)
                                }
                        
                        
                        line.append((0, 0, vals))
                            
                            
                    self.statements_line=line
            else:
                pass
                    
    def done(self):
        self.write({'state':'dept_approve'})
                
        
    def action_paid(self):
        self.write({'state':'paid'}) 
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
#         q=self.env['account.account'].search([('name','=','Bank'),('name','=','Loan')])
#         qc=self.env['account.account'].search([('name','=','Account Payable')])
        move_dict = {
              'name':self.name,
              'ref': self.name,
              'journal_id': self.journal_id.id,
              'date': self.date,
              'state': 'draft',
                   }
        debit_amount = self.loan_amount + self.interest_amount
        debit_line = (0, 0, {
#                      'move_id': move.id,
                'name': self.name,
                'debit': abs(debit_amount),
                'credit': 0.0,
                'account_id': self.debit_account_id.id,
                     })
        line_ids.append(debit_line)
        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
        if self.interest_account_id:
            credit_line = (0, 0, {
                              'name': self.name,
                              'debit': 0.0,
                              'credit': abs(self.interest_amount),
                              'account_id': self.interest_account_id.id,
                                      })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        if self.loan_account_id:
            credit_line = (0, 0, {
                              'name': self.name,
                              'debit': 0.0,
                              'credit': abs(self.loan_amount),
                              'account_id': self.loan_account_id.id,
                                      })
            line_ids.append(credit_line)
                
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
        
        
    
        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)
        
    
    def reset_to_approve(self):
        self.write({'state':'dept_approve'})    
         
    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == False:
            sequence = self.env.ref('openhcm_employee_loan.name_seq')
            vals['name'] = sequence.next_by_id()
        return super(employee_loanForm, self).create(vals)
    
    def action_view_journal(self):   
        po = self.env['account.move'].search([('ref', '=', self.name) ])
        action = self.env.ref('account.action_move_journal_line').read()[0]
        action['context'] = {
        'domain':[('id','in',po.ids)]
        
        }
        action['domain'] = [('id', 'in', po.ids)]
        return action 
    
    @api.onchange('statements_line')
    def get_lines_count(self):
        for s in self:
            q=0
            for ss in s.statements_line:
                q=q+1
        self.lines_count = q
        
    lines_count = fields.Integer(string='Installments', compute='get_lines_count')
    
    def paid_amount_total(self):
        for s in self:
            count=0
            if s:
                for ss in s.statements_line:
                    if ss.state=='paid':
                        count=count+ss.total
                
                    
                self.paid_amount=count
                
    def remaining_amount_total(self):
        for s in self:
            ct=0
            if s:
                for ss in s.statements_line:
                    if ss.state=='draft':
                        ct=ct+ss.total
                
                    
                self.remaining_amount=ct
                
                
    @api.model
    def _get_default_interest_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Interest'),],
            limit=1).id
    @api.model
    def _get_default_loan_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Loan'),],
            limit=1).id
    @api.model
    def _get_default_journal(self):
        return self.env['account.journal'].search([
            ('name', '=', 'Loan'),],
            limit=1).id
    
    @api.model
    def _get_default_debit_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Account Payable'),],
            limit=1).id
   
    name=fields.Char('Code',copy=False)
    employee_id =fields.Many2one('hr.employee',string="Employee",required=True)
    start_date=fields.Date("Start Date",required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', default=_get_default_journal,required=True)
    interest_account_id = fields.Many2one('account.account', string="Interest Account", default=_get_default_interest_account,required=True)
    loan_account_id = fields.Many2one('account.account', string="Loan Account", default=_get_default_loan_account,required=True)
    debit_account_id = fields.Many2one('account.account', string="Debit Account", default=_get_default_debit_account,required=True)    
    end_date=fields.Date("End Date")
    job_position=fields.Many2one('hr.job',string="Job Position")
    date=fields.Date("Date",default=datetime.today(),readonly=True)
    department=fields.Many2one('hr.department',"Department",compute="related_employee")
    manager_id=fields.Many2one('hr.employee', related='department.manager_id')
    payment_method=fields.Selection([('by_payslip','ByPayslip'),('other','Without Payslip')], string='Payment Method',required=True,default='by_payslip')
    type=fields.Many2one('employee.loan.type',string="Type",required=True)
    loan_amount=fields.Float('Loan Amount',required=True)
    interest_amount=fields.Float(string='Interest Amount',compute='interest_convert')
    extra_interest_amount=fields.Float(string='Extra Interest Amount')
    paid_amount=fields.Float(string='Paid Amount',compute='paid_amount_total')
    interest_rate=fields.Float(string='Interest Rate',required=True)
    remaining_amount=fields.Float(string='Remaining Amount',compute="remaining_amount_total")
    
    term=fields.Integer(string='Terms',required=True)
    user=fields.Many2one('res.users','User',default=lambda self: self.env.user,readonly=True)
    company_id=fields.Many2one('res.company','Company',readonly=True,default=lambda self:self.env.company.id)

    reason = fields.Text('Reason')
    statements_line=fields.One2many("employee.loan.installment","order_line")
    
    @api.onchange('name')
    def related_employee(self):
        for s in self:
            
            s.department=s.employee_id.department_id.id


    
class loan_installments_Form(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='employee.loan.installment'
    _description = 'This is Loan Installment'
    
    def action_paid(self):
        self.write({'state':'paid'})
    
    name=fields.Char("Name")
    date=fields.Date("Date")
    loan_amount=fields.Float(string='Loan Amount')
    total_interest=fields.Float(string='Total Interest')
    installment_amount=fields.Float(string='Installment Amount')
    interest=fields.Float(string='Interest')
    total=fields.Float(string='Total')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ], readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    order_line=fields.Many2one("employee.loan")   
    
class employee_loan_type(models.Model):
    _name='employee.loan.type'
    
    name=fields.Char("Name")
    
    
    
class rejected_approval(models.TransientModel):
    _name = 'refuse.order'
    _description = 'Create Refuse Wizard'
    
    refuse_d = fields.Text(string="Rejection Reason")
   
    
    def create_rejection(self):
        self.env['employee.loan'].browse(self._context.get('active_id')).update({'state':'refuse'}) 
        self.env['employee.loan'].browse(self._context.get('active_id')).update({'reason':self.refuse_d})


#class hr_loan_Form(models.Model):
 #   _inherit ='hr.payslip'
    
  #  def compute_sheet(self):
#         for other_input in self.input_line_ids:
#             other_input.unlink()
   #     level = super(hr_loan_Form, self).compute_sheet()
    #    other_inputs = self.env['hr.payslip.input.type'].search([('code','=', 'LOANINT'),('code','=', 'LOANINS')])
     #   paid_amount = self.env['employee.loan.installment'].search([('name','=', self.employee_id.id),('state','=', 'paid'),('date','>=', self.date_from),('date','<=', self.date_to)])
      #  data = []
       # amount = 0
        #for input in other_inputs:
         #   if input.code == 'LOANINS':
          #      for sal_amount in paid_amount:            
           #         amount = amount + sal_amount.installment_amount
            #    data.append((0,0,{
             #                   'payslip_id': self.id,
              #                  'sequence': 1,
               #                 'code': input.code,
                #                'contract_id': self.contract_id.id,
                 #               'input_type_id': input.id,
                  #              'amount': amount,
                   #             }))
            #self.input_line_ids = data
            #if input.code == 'LOANINT':
             #   for sal_amount in paid_amount:            
              #      amount = amount + sal_amount.interest
               # data.append((0,0,{
                #                'payslip_id': self.id,
                 #             'sequence': 1,
                  #              'code': input.code,
                   #             'contract_id': self.contract_id.id,
                    #            'input_type_id': input.id,
                     #           'amount': amount,
                      #          }))
            #self.input_line_ids = data
        #return level
        
#         lo_line=[]
#         if self.employee_id:
#             if self.date_from and self.date_to:
#                 lines = self.env['employee.loan'].search([('state','=','done')])
#                 for lin in lines:
#                     if lin.start_date and lin.end_date:
#                             if self.employee_id.id==lin.name.id:
#                                 for ss in lin.statements_line:
#                                     if ss.date<=self.date_from and ss.date<=self.date_to and ss.state=='draft':
#                                         vals = {
#                                                     'input_type_id':self.env['hr.payslip.input.type'].search([('code','=','LOAN')])[0].id,
#                                                     'amount':ss.total,
#                                                 }
                                        
                                        
#                                         lo_line.append((0, 0, vals))
                                
                                
#                 self.input_line_ids=lo_line                        
        
#    def action_payslip_done(self):
 #       
  #      levels = super(hr_loan_Form, self).action_payslip_done()
   #     if self.employee_id:
    #        if self.date_from and self.date_to:
     #           lines = self.env['employee.loan'].search([('state','=','done')])
      #          for lin in lines:
       #             if lin.start_date and lin.end_date:
        #                    if self.employee_id.id==lin.name.id:
         #                       for ss in lin.statements_line:
          #                          if ss.date<=self.date_from and ss.date<=self.date_to and ss.state=='draft':
           #                             ss.update({'state':'paid'})
        #return levels