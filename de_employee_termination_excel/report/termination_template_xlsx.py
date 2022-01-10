import json
from odoo import models
from odoo.exceptions import UserError
import xlwt


class TerminationXLSXReport(models.AbstractModel):
    _name = 'report.de_employee_termination_excel.report_emp_termination_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Terminated Employees')
        
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter'})
        # Merge 3 cells.
        sheet.merge_range('C2:D2', 'Employee Termination Report', merge_format)
        
        
        sheet.write(3, 0, 'Date From', format1)
        sheet.write(3, 1, str(data['date_from']), format1)
        sheet.write(3, 3, 'Date To', format1)
        sheet.write(3, 4, str(data['date_to']), format1)
        
        sheet.write(5, 0, 'SNO', format1)
        sheet.write(5, 1, 'Employee', format1)
        sheet.write(5, 2, 'Department', format1)
        sheet.write(5, 3, 'Job Title', format1)
        sheet.write(5, 4, 'Date Of Joining', format1)
        sheet.write(5, 5, 'Departure Date', format1)
        sheet.write(5, 6, 'Departure Reason', format1)
        sheet.write(5, 7, 'Additional Information', format1)

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 6
        sheet.set_column(row, 0, 20)
        sheet.set_column(row, 1, 20)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
        sheet.set_column(row, 4, 40)

        all_emp = self.env['hr.employee'].search([('active','=',False),('departure_date','>=',data['date_from']),('departure_date','<=',data['date_to'])])
        count = 1
        for emp in all_emp:
            sheet.write(row, 0, count, format2)
            sheet.write(row, 1, emp.name, format2)
            sheet.write(row, 2, str(emp.department_id.name), format2)
            sheet.write(row, 3, str(emp.job_title), format2)
            sheet.write(row, 4, str(emp.first_contract_date), format2)
            sheet.write(row, 5, str(emp.departure_date), format2)
            sheet.write(row, 6, emp.departure_reason, format2)
            sheet.write(row, 7, emp.departure_description, format2)
            
            count = count + 1
            row = row + 1
