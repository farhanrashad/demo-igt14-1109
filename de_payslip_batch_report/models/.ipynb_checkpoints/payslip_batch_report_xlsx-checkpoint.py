import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_payslip_batch_report.payslip_batch_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, line):
        #         raise UserError(data['id'])
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Payslip Batch Report')
        sheet.write(3, 0, 'Payslip REF', format1)
        sheet.write(3, 1, 'Account Name', format1)
        sheet.write(3, 2, 'Account No', format1)
        sheet.write(3, 3, 'Amount', format1)
        sheet.write(3, 4, 'Currency', format1)

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
        sheet.set_column(row, 4, 20)
        
        currency_obj = self.env['res.currency'].search([('id','=',data['currency'])], limit=1)

        employees = self.env['hr.employee'].search([])
        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', data['id'])])
        for payslip in payslips:
            sheet.write(row, 0, payslip.number, format2)
            sheet.write(row, 1, payslip.employee_id.bank_account_id.acc_holder_name, format2)
            sheet.write(row, 2, payslip.employee_id.bank_account_id.acc_number, format2)
            sheet.write(row, 3, payslip.net_wage, format2)
            sheet.write(row, 4, (str(currency_obj.name)), format2)

            row = row + 1
