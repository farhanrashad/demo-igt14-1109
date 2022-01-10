# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

import logging
from odoo import models


class ReportGeneralLedgerExcel(models.Model):
    _name = "report.accounting_excel_reports.report_generalledger_excel"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_general_ledger']
        results = report_obj._get_report_values(obj, data)
        sheet = workbook.add_worksheet()

        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True, 'bg_color': '#bfbfbf', 'valign': 'vcenter'})
        format2 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format3 = workbook.add_format({'font_size': 12, 'align': 'right', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format4 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format5 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format6 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'text_wrap': 'true'})
        format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format8 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'num_format': 'yyyy-mm-dd'})

        sheet.set_row(0, 40)
        sheet.set_row(2, 40)
        sheet.set_column(0, 1, 13)
        sheet.set_column(2, 5, 25)
        sheet.set_column(6, 8, 15)

        sheet.merge_range('A1:I1', "General Ledger Report", format1)
        account_list = ' '
        account_list_code = self.env['account.account'].search([('id','in', results['account_codes'])])
        for account_line in account_list_code:
            account_list = account_list +  str(account_line.code +' '+ account_line.name)+ ', '    
        sheet.merge_range('A3:B3', "Account", format4)
        sheet.write('C3', str(account_list), format6)
        sheet.write('G3', 'Target Moves', format4)
        if data['form']['target_move'] == 'posted':
            sheet.merge_range('H3:I3', 'All Posted Entries', format6)
        else:
            sheet.write('H3:I3', 'All Entries', format6)

        sheet.merge_range('A4:B4', "Display Account", format4)
        if data['form']['display_account'] == 'all':
            sheet.write('C4', 'All', format6)
        elif data['form']['display_account'] == 'movement':
            sheet.write('C4', 'With Movements', format6)
        else:
            sheet.write('C4', 'With balance is not equal to 0', format6)
        sheet.write('G4', 'Sorted By', format4)
        if data['form']['sortby'] == 'sort_date':
            sheet.merge_range('H4:I4', 'Date', format6)
        else:
            sheet.write('H4:I4', 'Journal & Partner', format6)

        if data['form']['date_from']:
            sheet.merge_range('A5:B5', "Date From", format4)
            sheet.write('C5', data['form']['date_from'], format6)
        if data['form']['date_to']:
            sheet.write('G5', "Date To", format4)
            sheet.merge_range('H5:I5', data['form']['date_to'], format6)

        sheet.write('A7', "Date ", format2)
        sheet.write('B7', "JRNL", format2)
        sheet.write('C7', "Partner", format2)
        sheet.write('D7', "Counterpart", format2)
        sheet.write('E7', "Ref", format2)
        sheet.write('F7', "Financial Period", format2)
        sheet.write('G7', "Employee", format2)
        sheet.write('H7', "Department", format2)
        sheet.write('I7', "Project", format2)
        sheet.write('J7', "Analytic Account", format2)
        sheet.write('K7', "Move", format2)
        sheet.write('L7', "Entry Label", format2)
        sheet.write('M7', "Debit", format3)
        sheet.write('N7', "Credit", format3)
        sheet.write('O7', "Balance", format3)
        sheet.write('P7', "Company Currency", format3)
        sheet.write('Q7', "Amount In Currency", format3)
        sheet.write('R7', "Document Currency", format3)
        currency_obj = self.env['res.currency'].search([('id','=',data['currency_id'])])
        company_currency = self.env.company.id
        bc_company_obj = self.env['res.company'].search([('id','=',company_currency)])
        bc_currency_obj = bc_company_obj.currency_id
        bc_currency_symbol = bc_currency_obj.symbol
        company_currency_name = self.env.company.currency_id.name
        company_currency_symbol = self.env.company.currency_id.symbol
        row = 7
        col = 0
        for account in results['Accounts']:
            
#             sheet.merge_range(row, col, row, col + 10, account['code'] + account['name'], format4)
            sheet.write(row, col + 1, str(), format5)
            sheet.write(row, col + 2, str(), format5)
            sheet.write(row, col + 3, str(), format5)
            sheet.write(row, col + 4, str(), format5)
            sheet.write(row, col + 5, str(), format5)
            sheet.write(row, col + 6, str(), format5)
            sheet.write(row, col + 7, str(), format5)
            sheet.write(row, col + 8, str(), format5)
            sheet.write(row, col + 9, str(), format5)
            sheet.write(row, col + 10, str(), format5)
            sheet.write(row, col + 11, str(), format5)
            sheet.write(row, col + 12, (account['debit']), format5)
            sheet.write(row, col + 13, (account['credit']), format5)
            sheet.write(row, col + 14, (account['debit'] - account['credit']), format5)
            
            sheet.write(row, col + 15, str(), format5)
            sheet.write(row, col + 16, str(), format5)
            sheet.write(row, col + 17, str(), format5)
            total_debit = 0.0
            total_credit = 0.0
            total_balance = 0.0
            total_amount_currency = 0.0  
            for line in account['move_lines']:
                counterpart = self.env['account.move.line'].search([('move_id.name','=',line['move_name'])])
                account_code1 = 0
                for counter_line in counterpart:
                    if counter_line.debit== 0.0:
                        account_code1 = counter_line.account_id.code    
                col = 0
                row += 1
                total_debit += line['debit']
                total_credit += line['credit']
                total_balance += (line['debit'] - line['credit'])
                total_amount_currency += line['amount_currency']
                
                sheet.write(row, col, line['ldate'], format8)
                sheet.write(row, col + 1, line['lcode'], format6)
                sheet.write(row, col + 2, line['partner_name'], format6)
                sheet.write(row, col + 3, str(account_code1), format6)
                sheet.write(row, col + 4, line['lref'] or '', format6)
                sheet.write(row, col + 5, line['account_period'], format6)
                sheet.write(row, col + 6, line['employee_name'], format6)
                sheet.write(row, col + 7, line['department_name'], format6)
                sheet.write(row, col + 8, line['project_name'], format6)
                sheet.write(row, col + 9, line['analytic_account'], format6)
                sheet.write(row, col + 10, line['move_name'], format6)
                sheet.write(row, col + 11, line['lname'], format6)
                sheet.write(row, col + 12, (line['debit']), format7)
                sheet.write(row, col + 13, (line['credit']), format7)
                sheet.write(row, col + 14, (line['debit'] - line['credit']), format7)
                sheet.write(row, col + 15, (company_currency_name +' ('+company_currency_symbol+')'), format7)
                sheet.write(row, col + 16, (line['amount_currency']), format7)
                sheet.write(row, col + 17, (line['currency_name'] +' ('+line['currency_code']+')'), format7)

            row += 1
            sheet.write(row, col + 0, str(), format7)
            sheet.write(row, col + 1, str("Total"), format7)
            sheet.write(row, col + 2, str(), format7)
            sheet.write(row, col + 3, str(), format7)
            sheet.write(row, col + 4, str(), format7)
            sheet.write(row, col + 5, str(), format7)
            sheet.write(row, col + 6, str(), format7)
            sheet.write(row, col + 7, str(), format7)
            sheet.write(row, col + 8, str(), format7)
            sheet.write(row, col + 9, str(), format7)
            sheet.write(row, col + 10, str(), format7)
            sheet.write(row, col + 11, str(), format7)
            sheet.write(row, col + 12, str(total_debit), format7)
            sheet.write(row, col + 13, str(total_credit), format7)
            sheet.write(row, col + 14, str(total_balance), format7)
            
            sheet.write(row, col + 15, str(total_amount_currency), format7)
            sheet.write(row, col + 16, str(), format7)
            sheet.write(row, col + 17, str(), format7)
