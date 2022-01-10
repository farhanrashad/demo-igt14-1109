import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_active_lease.report_active_lease'
    _description = 'Active Lease Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Active Lease')
        #sheet.merge_range('C2:E2', 'Active Lease Report', format0)
        #sheet.write(1, 4, 'Active Lease Report', format0)
        #sheet.write(3, 0, 'Report On', format0)
        #sheet.write(3, 1, in_date, format0)
        
        
        sheet.write(1, 0, 'LA', format1)
        sheet.write(1, 1, 'Region', format1)
        sheet.write(1, 2, 'Site Name', format1)
        sheet.write(1, 3, 'Landlord', format1)
        sheet.write(1, 4, 'Candidate', format1)
        sheet.write(1, 5, 'Lease Hunter Name', format1)
        sheet.write(1, 6, 'Start Date', format1)
        sheet.write(1, 7, 'End Date', format1)
        sheet.write(1, 8, 'Original Amount', format1)
        sheet.write(1, 9, 'Current Amount', format1)
        sheet.write(1, 10, 'Total Commitment', format1)
        sheet.write(1, 11, 'Total Invoiced', format1)
        sheet.write(1, 12, 'Total Paid', format1)
        sheet.write(1, 13, 'Paid Upto', format1)
        sheet.write(1, 14, 'Open Commitment', format1)
        sheet.write(1, 15, 'Stamp Duty', format1)
        sheet.write(1, 16, 'Registration', format1)
        sheet.write(1, 17, 'RFI Date', format1)
        sheet.write(1, 18, 'Partner Reference (NRC)', format1)
        sheet.write(1, 19, 'Phone No.', format1)
        sheet.write(1, 20, 'Key Contact (Bank Information)', format1)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 2
        purchase_subscritpion_ids = self.env['purchase.subscription'].search([('allow_lease','=',True),('stage_category','in',['confirm','progress'])])
        bank = ''
        dated = ''
        for sub in purchase_subscritpion_ids:
            for bank in sub.partner_id.bank_ids:
                bank = bank.bank_id.name + '-' + bank.acc_number
            for line in sub.purchase_subscription_schedule_line:
                if line.invoice_id:
                    dated = line.date_to.strftime("%d/%m/%Y")
                else:
                    break
            sheet.write(row, 0, sub.name, format2)
            sheet.write(row, 1, sub.project_id.state_id.name, format2)
            sheet.write(row, 2, sub.project_id.name, format2)
            sheet.write(row, 3, sub.partner_id.name, format2)
            sheet.write(row, 4, sub.candidate, format2)
            sheet.write(row, 5, sub.lease_hunter_partner_id.name, format2)
            sheet.write(row, 6, sub.date_start.strftime("%d/%m/%Y"), format2)
            sheet.write(row, 7, sub.date.strftime("%d/%m/%Y"), format2)
            sheet.write(row, 8, sub.amount_lease_original, format2)
            sheet.write(row, 9, sub.amount_lease_current, format2)
            sheet.write(row, 10, sub.amount_lease_total, format2)
            sheet.write(row, 11, sub.recurring_billed_total, format2)
            sheet.write(row, 12, sub.recurring_paid_total, format2)
            sheet.write(row, 13, dated, format2)
            sheet.write(row, 14, (sub.amount_lease_total - sub.recurring_paid_total), format2)
            sheet.write(row, 15, sub.allow_stamp_duty, format2)
            sheet.write(row, 16, sub.allow_registration, format2)
            sheet.write(row, 17, sub.project_id.date_rfi, format2)
            sheet.write(row, 18, sub.allow_registration, format2)
            sheet.write(row, 19, sub.partner_id.phone, format2)
            sheet.write(row, 20, sub.partner_id.bank_key_contact, format2)
            row = row + 1
        