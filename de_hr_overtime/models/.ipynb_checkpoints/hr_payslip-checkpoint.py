# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval

class HRPayslip(models.Model):
    _inherit = 'hr.payslip'

    overtime_ids = fields.Many2many('hr.overtime.request')
    overtime_line_ids = fields.Many2many('hr.overtime.request.line')
    
    date_from_overtime = fields.Date(string='From Overtime', compute='_compute_overtime_duration', states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})
    date_to_overtime = fields.Date(string='To Overtime', compute='_compute_overtime_duration', states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})
    #date_to_overtime = fields.Date(string='To Overtime', readonly=True, required=True, default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})

    @api.depends('date_from','date_to')
    def _compute_overtime_duration(self):  
        dt1 = dt2 = False
        fdays = -15
        tdays = 14
        for payslip in self:
            if payslip.date_from:
                dt1 = fields.Date.to_string(payslip.date_from + timedelta(fdays))
                dt2 = fields.Date.to_string(payslip.date_from + timedelta(tdays))
        self.date_from_overtime = dt1
        self.date_to_overtime = dt2
        
    #@api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        #res = super(HRPayslip, self).onchange_employee()
        lst = []
        if self.date_from and self.date_to and self.contract_id:
            self._cr.execute("select count(id), sum(overtime_amount) from hr_overtime_request where date_from::date>='%s' and date_to::date<='%s' and employee_id=%d" % (self.date_from, self.date_to, self.employee_id.id))
            result = self._cr.fetchone()
            if result and result[0]:
                lst.append({'name': '%s Overtime' % (self.employee_id.name),
                            'number_of_days': result[0],
                            'number_of_hours': result[1],
                            'code' : 'OT100',
                            'amount': 100,
                            'contract_id': self.contract_id.id})
            
        #self.worked_days_line_ids = False
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in lst:
            worked_days_lines += worked_days_lines.new(r)
            r['amount'] = 200
        self.worked_days_line_ids += worked_days_lines
        #return res
    
    def compute_sheet(self):
        amount = 0 
        overtime = False
        #day based overtime calcualtion
        for payslip in self:
            overtime = self.env['hr.overtime.request.line'].search([('employee_id', '=', payslip.employee_id.id),('state', '=', 'approved'),('type', '=', 'cash'),('date_overtime', '>=', payslip.date_from_overtime),('date_overtime', '<=', payslip.date_to_overtime)])
            if overtime:
                for ot_obj in overtime:
                    if ot_obj:
                        amount += ot_obj.approved_amount
                    #amount = 40
            
                input_exists = self.env['hr.payslip.input'].search([('payslip_id', '=', payslip.id), ('code', '=', 'OT100')])              
                if not input_exists:
                    input_type_exists = self.env['hr.payslip.input.type'].search([('code', '=', 'OT100')])   
                    input_exists.create({
                        'input_type_id': input_type_exists.id,
                        'code': 'OT100',
                        'amount': amount,
                        'contract_id': payslip.contract_id.id,
                        'payslip_id': payslip.id,
                    })
                else:
                    input_exists.write({
                        'amount': amount,
                    })
            payslip.overtime_line_ids = overtime
        rec = super(HRPayslip, self).compute_sheet()
        return rec
    

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        """
        function used for writing overtime record in payslip
        input tree.

        """
        res = super(HRPayslip, self).get_inputs(contracts, date_to, date_from)
        overtime_type = self.env.ref('de_hr_overtime.hr_salary_rule_overtime')
        contract = self.contract_id
        overtime_id = self.env['hr.overtime.request'].search([('employee_id', '=', self.employee_id.id),
                                                      ('contract_id', '=', self.contract_id.id),
                                                      ('state', '=', 'approved'), ('payslip_paid', '=', False)])
        hrs_amount = overtime_id.mapped('cash_hrs_amount')
        day_amount = overtime_id.mapped('cash_day_amount')
        cash_amount = sum(hrs_amount) + sum(day_amount)
        if overtime_id:
            self.overtime_ids = overtime_id
            input_data = {
                'name': overtime_type.name,
                'code': overtime_type.code,
                'amount': cash_amount,
                'contract_id': contract.id,
            }
            res.append(input_data)
        return res

    def action_payslip_done(self):
        """
        function used for marking paid overtime
        request.

        """
        for line in self.overtime_line_ids:
            if line.overtime_request_id:
                line.overtime_request_id.state = 'paid'
                
        for recd in self.overtime_ids:
            if recd.type == 'cash':
                recd.payslip_paid = True
        return super(HRPayslip, self).action_payslip_done()
