from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
from datetime import date
import calendar


class EmployeeMissingAttandanceWizard(models.Model):
    _name = "employee.termination.wizard"
    _description = "Employee Termination Wizard"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    
    def print_employee_termination_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to'])[0]
        return self.env.ref('de_employee_termination_excel.action_termination_pdf_report').report_action(self, data=data, config=False)
    
    
    
    def print_employee_termination_xlsx(self):
        datas = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('de_employee_termination_excel.action_termination_xlsx').report_action(self,data=datas)    
    
    
    