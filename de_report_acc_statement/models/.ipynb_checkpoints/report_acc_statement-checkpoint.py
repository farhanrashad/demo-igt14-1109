import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_acc_statement.report_acc_statement'
    _description = 'Account Statement Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        f_date = data['date_from']
        f_date = datetime.strptime(f_date, '%Y-%m-%d')
        f_date = f_date.strftime("%d/%m/%Y")
        
        t_date = data['date_to']
        t_date = datetime.strptime(t_date, '%Y-%m-%d')
        t_date = t_date.strftime("%d/%m/%Y")
        
        date = str(f_date) + " to " + str(t_date)
        
        domain = domain1 = []
        date_heading = ''
        if data['date_from']:
            domain += [('date','>=',data['date_from'])]
        if data['date_to']:
            domain += [('date','<=',data['date_to'])]
        
        if data['partner_ids']:
            list_partner_ids = self.env['res.partner'].search([('id', 'in', data['partner_ids'])])
            partner_ids = tuple([pro_id.id for pro_id in list_partner_ids])
            domain += [('partner_id','in',partner_ids)]
            
            #domain += [('partner_id','in',data['partner_ids'])]
            
        
        format0 = workbook.add_format({'font_size': '16', 'align': 'left', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': True, 'bg_color': 'yellow', 'border':True})
        
        sheet = workbook.add_worksheet('Account Statement Report')
        sheet.merge_range('A2:K2', 'Account Statement Report', format0)
        sheet.write(1, 4, 'Account Statement Report', format0)
        sheet.merge_range('A3:K3', 'Date', format0)
        sheet.write(1, 6, 'Report On', format0)
        sheet.write(3, 1, date, format0)
        
        
        sheet.set_column(6, 0, 35)
        sheet.set_column(6, 1, 20)
        sheet.set_column(6, 2, 20)
        sheet.set_column(6, 3, 20)
        sheet.set_column(6, 4, 20)
        sheet.set_column(6, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(6, 7, 20)
        sheet.set_column(6, 8, 20)
        sheet.set_column(6, 9, 20)
        sheet.set_column(6, 10, 20)
        sheet.set_column(6, 11, 20)
            
        sheet.write(6, 0, 'Customer', format1)
        sheet.write(6, 1, 'Invoice Date', format1)
        sheet.write(6, 2, 'Number', format1)
        sheet.write(6, 3, 'Category', format1)
        sheet.write(6, 4, 'Due Date', format1)
        sheet.write(6, 5, 'Invoice Currency', format1)
        sheet.write(6, 6, 'Billing Month', format1)
        sheet.write(6, 7, 'Description', format1)
        sheet.write(6, 8, 'Untax Total', format1)
        sheet.write(6, 9, 'Commercial Tax', format1)
        sheet.write(6, 10, 'Total Amount', format1)
        sheet.write(6, 11, 'Residual', format1)
        
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'center', 'border': True})
        format3 = workbook.add_format({'font_size': '12', 'align': 'right', 'border':True, 'num_format':'#,##0.00'})
        row = 7
       
        
        in_qty = out_qty = 0
        
        moves = self.env['account.move'].search(domain)                
        for move in moves.filtered(lambda x: x.move_type in ['out_invoice','out_refund'] and x.state in ['posted'] and x.payment_state in ['not_paid','partial']):
        
            sheet.write(row, 0, move.partner_id.name, format2)
            sheet.write(row, 1, move.invoice_date.strftime("%d/%m/%Y"), format2)
            sheet.write(row, 2, move.name, format2)
            sheet.write(row, 3, move.category, format2)
            sheet.write(row, 4, move.invoice_date_due.strftime("%d/%m/%Y"), format2)
            sheet.write(row, 5, move.currency_id.name, format2)
            sheet.write(row, 6, move.account_period, format2)
            sheet.write(row, 7, move.payment_reference, format2)
            sheet.write(row, 8, move.amount_untaxed, format3)
            sheet.write(row, 9, (move.amount_total-move.amount_untaxed), format3)
            sheet.write(row, 10, move.amount_total, format3)
            sheet.write(row, 11, move.amount_residual, format3)
            #sheet.write(row, 11, sub.project_id.date_rfi, format2)
            row = row + 1
        