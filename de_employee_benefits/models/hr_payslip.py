# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    work_location = fields.Char(related='employee_id.work_location')   
    bank_account_id = fields.Many2one(related='employee_id.bank_account_id')   
    job_id = fields.Char(related='employee_id.job_title') 
    conctract_type = fields.Selection(related='employee_id.type', string='Contract Type') 
    
    @api.constrains('contract_id')
    def onchange_employee_input(self):
    	for payslip in self:
	        for other_input in self.input_line_ids:
	            other_input.unlink()
	            
	        data = []
	        if self.contract_id:
	            contract_type = self.env['hr.contract'].search([('id','=', self.contract_id.id),('state','=', 'open')])

	            for contract in contract_type:            
	                for cont_line in contract.benefit_line_ids:               
	                    data.append((0,0,{
	                                    'input_type_id': cont_line.input_type_id.id,
	                                    'amount': cont_line.amount,
	                                    }))
	                self.input_line_ids = data



