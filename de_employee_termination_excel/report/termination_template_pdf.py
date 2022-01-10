import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from odoo import api, fields, models, _
from datetime import date, timedelta
import pytz


class TerminationReportPDF(models.AbstractModel):
    _name = 'report.de_employee_termination_excel.termination_template'
    
    
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        all_emp = self.env['hr.employee'].search([('active','=',False),('departure_date','>=',date_from),('departure_date','<=',date_to)])
        
        print('all_emp====',all_emp)

        return {
            'doc_ids': self.ids,
            'doc_model': 'hr_attendance.hr.attendance',
            'date_from': data['form']['date_from'],
            'date_to': data['form']['date_to'],
            'all_emp': all_emp,
        }