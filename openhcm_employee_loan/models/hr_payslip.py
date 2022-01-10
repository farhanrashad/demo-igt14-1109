from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from datetime import datetime
from dateutil.relativedelta import relativedelta

   



class hr_loan_Form(models.Model):
    _inherit ='hr.payslip'
    
    
    installment_ids = fields.Many2many('employee.loan.installment', string='Installment Lines', domain="[('state', '=', 'draft'),('order_line.state','=', 'done'),('order_line.employee_id','=', employee_id)]")
    
    def compute_sheet(self):
        for order in self:
            for other_input in order.input_line_ids:
                 other_input.unlink()
            loan_inputs = self.env['hr.payslip.input.type'].search([('code','=', 'LOANINS')])
            inrest_inputs = self.env['hr.payslip.input.type'].search([('code','=', 'LOANINT')])
            data = []
            amount = 0
            interset = 0
            for input in loan_inputs:
                if input.code == 'LOANINS':
                    for sal_amount in order.installment_ids:            
                        amount = amount + sal_amount.installment_amount
                data.append((0,0,{
                                    'payslip_id': order.id,
                                    'sequence': 1,
                                    'code': input.code,
                                    'contract_id': order.contract_id.id,
                                    'input_type_id': input.id,
                                    'amount': amount,
                                    }))
                order.input_line_ids = data
            if input.code == 'LOANINT':
                for input in inrest_inputs:
                    for sal_amount in order.installment_ids:            
                        interset = interset + sal_amount.interest
                    data.append((0,0,{
                                        'payslip_id': order.id,
                                        'sequence': 1,
                                        'code': input.code,
                                        'contract_id': order.contract_id.id,
                                        'input_type_id': input.id,
                                        'amount': interset,
                                        }))
                order.input_line_ids = data
        level = super(hr_loan_Form, self).compute_sheet()
        return level

    def action_payslip_done(self):        
        levels = super(hr_loan_Form, self).action_payslip_done()
        if self.employee_id:
            for line in self.installment_ids:
                line.update({'state':'paid'})
        return levels
        
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

     
                       
        
   # def action_payslip_done(self):
        
    #    levels = super(hr_loan_Form, self).action_payslip_done()
    #    if self.employee_id:
     #       if self.date_from and self.date_to:
      #          lines = self.env['employee.loan'].search([('state','=','done')])
       #         for lin in lines:
        #            if lin.start_date and lin.end_date:
         #                   if self.employee_id.id==lin.name.id:
          #                      for ss in lin.statements_line:
           #                         if ss.date>=self.date_from and ss.date<=self.date_to and ss.state=='draft':
            #                            ss.update({'state':'paid'})
       # return levels