# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_account_aging.report_account_aging'
    _description = 'Account Aging Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        from_date = data['from_date']
        from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        from_date = from_date.strftime("%d/%m/%Y")
        
        to_date = data['to_date']
        to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime("%d/%m/%Y")
        
        
        format0 = workbook.add_format({'font_size': '18', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        #For SPMRF
        sheet = workbook.add_worksheet('Aged Receivable Balance Report')
        sheet.merge_range('C2:E2', 'Aged Receivable Balance Report', format0)
        sheet.write(3, 0, 'From Date', format0)
        sheet.write(3, 1, from_date, format0)
        sheet.write(4, 0, 'To Date', format0)
        sheet.write(4, 1, to_date, format0)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        
        sheet.write(6, 0, 'Partners', format1)
        sheet.write(6, 1, 'Not Due', format1)
        sheet.write(6, 2, '0-30', format1)
        sheet.write(6, 3, '30-60', format1)
        sheet.write(6, 4, '60-90', format1)
        sheet.write(6, 5, '90-120', format1)
        sheet.write(6, 6, '+120', format1)
        sheet.write(6, 7, 'Total', format1)
        
        
        domain = domain1 = location_name = ''
        
        domain = [('invoice_date','>=',data['from_date'])]
        domain += [('invoice_date','<=',data['to_date'])]
        domain += [('state','=','posted')]
        if data['partner_ids']:
            domain += [('partner_id','in',data['partner_ids'])]
            
        account_moves = self.env['account.move'].search([])
        
        customers_list = []
        all_move_ids = self.env['account.move'].search(domain)
        for p in all_move_ids.partner_id:
            if p not in customers_list:
                customers_list.append(p)
                
        row = 7
        due1 = due2 = due3 = due4 = due5 = 0
        amt1 = amt2 = amt3 = amt4 = amt5 = tot = 0
        fmt = '%Y-%m-%d'

        for cust in customers_list:
            domain1 = domain + [('partner_id','=',cust.id)]
            account_moves = self.env['account.move'].search(domain1)
            sheet.write(row, 0, cust.name, format2)
            amt1 = amt2 = amt3 = amt4 = amt5 = tot = 0
            for move in account_moves:
                if move.invoice_date:
                    tot += move.amount_total_signed
                    if (fields.date.today() - move.invoice_date).days > 0 and (fields.date.today() - move.invoice_date).days <= 30:
                        due1 = (fields.date.today() - move.invoice_date).days
                        amt1 += move.amount_total_signed
                    elif (fields.date.today() - move.invoice_date).days > 30 and (fields.date.today() - move.invoice_date).days <= 60:
                        due2 = (fields.date.today() - move.invoice_date).days
                        amt2 += move.amount_total_signed
                    elif (fields.date.today() - move.invoice_date).days > 60 and (fields.date.today() - move.invoice_date).days <= 90:
                        due3 = (fields.date.today() - move.invoice_date).days
                        amt3 += move.amount_total_signed
                    elif (fields.date.today() - move.invoice_date).days > 90 and (fields.date.today() - move.invoice_date).days <= 120:
                        due4 = (fields.date.today() - move.invoice_date).days
                        amt4 += move.amount_total_signed
                    elif (fields.date.today() - move.invoice_date).days > 120:
                        due5 = (fields.date.today() - move.invoice_date).days
                        amt5 += move.amount_total_signed
            sheet.write(row, 1, tot, format2)
            sheet.write(row, 2, amt1, format2)
            sheet.write(row, 3, amt2, format2)
            sheet.write(row, 4, amt3, format2)
            sheet.write(row, 5, amt4, format2)
            sheet.write(row, 6, amt5, format2)
            sheet.write(row, 7, (amt1+amt2+amt3+amt4+amt5), format2)
            row = row + 1
        