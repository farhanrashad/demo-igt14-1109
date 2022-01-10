# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar



class EmployeeAttandanceWizard(models.Model):
    _name = "employee.attendance.wizard"
    _description = "Employee Wizard"
    
    
#     declaring attandance wizard fields
    current_date=fields.Date(string="Date",default=datetime.datetime.today())
    month = fields.Selection([("1", 'January'), ("2", 'February'), ("3", 'March'), ("4", 'April'),
                              ("5", 'May'), ("6", 'June'), ("7", 'July'), ("8", 'August'),
                              ("9", 'September'), ("10", 'October'), ("11", 'November'), ("12", 'December')],
                             string='Month',default=str(datetime.datetime.today().month))
    print_by = fields.Selection([('daily', 'Daily'),
                                   ('weekly', 'Weekly'),
                                 ('monthly', 'Monthly')],default="daily")
    all_emp=fields.Boolean(string="All Employees")
    employee=fields.Many2many('hr.employee',string="Employee")





    @api.onchange('all_emp')
    def _get_sel_emp(self):
        if self.all_emp==True:
            print("it was true--------------")
            return
        else:
            print("it was false------------")
            self.all_emp=False

    def action_report_gen(self):
        print("called action report gen----------------------------")
        #for months report
        year = int(datetime.datetime.today().year)
        month = int(self.month)
        print("month is : ",month,type(month))
        x = calendar.monthrange(year, month)
        print(x)
        print(year)
        num_days_c = x[1]
        print(num_days_c)
        num_days = calendar.monthrange(year, month)[1]
        days_for_month = [str(datetime.date(year, month, day)) for day in range(1, num_days + 1)]
        print(days_for_month)
        #month report end
        emp_name={}
        count=0
        for temp in self.employee:
                emp_name[self.employee[count].id]=self.employee[count].name
                count=count+1
        print("selected emp  ara------------",emp_name)
        if not self.current_date:
            raise UserError(_("Please Select Date"))
            return
        datas = {
            'current_date': self.current_date,
            'print_by': self.print_by,
            'all_emp': self.all_emp,
            'emp_sel':emp_name,
            'days_for_month':days_for_month
        }
        return self.env.ref('openhcm_employee_attendance.emp_att_xlsx').report_action(self,data=datas)