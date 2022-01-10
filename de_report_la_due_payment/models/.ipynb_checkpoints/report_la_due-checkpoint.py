
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_la_due_payment.report_la_due'
    _description = 'Lease Due Payment Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        f_date = data['date_from']
        f_date = datetime.strptime(f_date, '%Y-%m-%d')
        f_date = f_date.strftime("%d/%m/%Y")
        
        t_date = data['date_to']
        t_date = datetime.strptime(t_date, '%Y-%m-%d')
        t_date = t_date.strftime("%d/%m/%Y")
        
        date = str(f_date) + " to " + str(t_date)
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Lease Due Payment Report')
        sheet.merge_range('C2:E2', 'Lease Due Payment Report', format0)
        sheet.write(1, 4, 'Lease Due Payment Report', format0)
        sheet.write(3, 0, 'Report On', format0)
        sheet.write(3, 1, date, format0)

        sheet.write(6, 0, 'LA', format1)
        sheet.write(6, 1, 'Landlord', format1)
        sheet.write(6, 2, 'Site Name', format1)
        sheet.write(6, 3, 'Candidate', format1)
        sheet.write(6, 4, 'Region', format1)
        sheet.write(6, 5, 'Date From', format1)
        sheet.write(6, 6, 'Date To', format1)
        sheet.write(6, 7, 'No. of Months', format1)
        sheet.write(6, 8, 'Monthly Amount', format1)
        sheet.write(6, 9, 'Total Amount', format1)
        sheet.write(6, 10, 'Paid Up To', format1)
        sheet.write(6, 11, 'RFI Date', format1)
        sheet.write(6, 12, 'Partner Reference (NRC)', format1)
        sheet.write(6, 13, 'Key Contact (Bank Information)', format1)
        sheet.write(6, 14, 'Status', format1)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'center'})
        format3 = workbook.add_format({'font_size': '12', 'align': 'right', 'num_format':'#,##0.00'})
        
        row = 7
       
        domain = domain1 = location_name = ''
        in_qty = out_qty = 0
        
        domain = [('date','<=',data['date_from'])]
        paid_upto_date = False
        purchase_subscritpion_ids = self.env['purchase.subscription'].search([('allow_lease','=',True)])
        schedule_lines = self.env['purchase.subscription.schedule']
        project_id = self.env['project.project']
        bank = ''
        for sub in purchase_subscritpion_ids:
            schedule_lines = self.env['purchase.subscription.schedule'].search([('purchase_subscription_id','=',sub.id)])
            for schedule in schedule_lines:
                if schedule.invoice_id.payment_state in ('in_payment','partial'):
                    paid_upto_date = schedule.date_to.strftime("%d/%m/%Y")
                    
            for bank in sub.partner_id.bank_ids:
                bank = bank.bank_id.name + '-' + bank.acc_number
                
            for line in sub.purchase_subscription_schedule_line.filtered(lambda x: str(x.date_from) >= data['date_from'] and str(x.date_from) <= data['date_to']):
            #for line in schedule_lines:
                sheet.write(row, 0, sub.name, format2)
                sheet.write(row, 1, sub.partner_id.name, format2)
                sheet.write(row, 2, sub.project_id.name, format2)
                if sub.candidate:
                    sheet.write(row, 3, sub.candidate, format2)
                sheet.write(row, 4, sub.project_id.state_id.name, format2)
                sheet.write(row, 5, line.date_from.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 6, line.date_to.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 7, line.recurring_intervals, format2)
                sheet.write(row, 8, line.recurring_monthly_total, format3)
                sheet.write(row, 9, line.recurring_total, format3)
                if paid_upto_date:
                    sheet.write(row, 10, paid_upto_date, format2)
                if sub.project_id.date_rfi:
                    sheet.write(row, 11, sub.project_id.date_rfi.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 12, sub.partner_id.ref, format2)
                if sub.partner_id.bank_key_contact:
                    sheet.write(row, 13, sub.partner_id.bank_key_contact, format2)
                sheet.write(row, 14, sub.stage_id.name, format2)
                
                row = row + 1
        