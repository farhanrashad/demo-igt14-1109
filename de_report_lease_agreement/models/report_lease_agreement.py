import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_lease_agreement.report_lease_agreement'
    _description = 'Lease Agreement Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        in_date = data['date_from']
        #in_date = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
        #in_date = in_date.strftime("%d/%m/%Y")
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Lease Agreement Report')
        sheet.merge_range('C2:E2', 'Lease Agreement Report', format0)
        sheet.write(1, 4, 'Lease Agreement Report', format0)
        sheet.write(3, 0, 'Report On', format0)
        sheet.write(3, 1, (data['date_from'] + " to " + data['date_to']), format0)
 
        sheet.write(6, 0, 'Lease Agreement', format1)
        sheet.write(6, 1, 'Lease Agreement Start Date', format1)
        sheet.write(6, 2, 'Lease Agreement End Date', format1)
        sheet.write(6, 3, 'Site', format1)
        sheet.write(6, 4, 'Region', format1)
        sheet.write(6, 5, 'Landlord Name', format1)
        sheet.write(6, 6, 'Landlord Address', format1)
        sheet.write(6, 7, 'Landlord Phone', format1)
        sheet.write(6, 8, 'Landlord Mobile', format1)
        sheet.write(6, 9, 'Lease Hunter Name', format1)
        sheet.write(6, 10, 'Product', format1)
        sheet.write(6, 11, 'Cost Center', format1)
        sheet.write(6, 12, 'Registration', format1)
        sheet.write(6, 13, 'Date of Registration', format1)
        sheet.write(6, 14, 'Stamp Duty', format1)
        sheet.write(6, 15, 'Date of Stamp Duty', format1)
        sheet.write(6, 16, 'Original Amount', format1)
        sheet.write(6, 17, 'Current Amount', format1)
        sheet.write(6, 18, 'Total Commitment', format1)
        sheet.write(6, 19, 'Total Invoiced', format1)
        sheet.write(6, 20, 'Total Paid', format1)
        sheet.write(6, 21, 'Open Commitment', format1)
        sheet.write(6, 22, 'Currency', format1)
        sheet.write(6, 23, 'Payment Schedule Date From', format1)
        sheet.write(6, 24, 'Payment Schedule Date To', format1)
        sheet.write(6, 25, 'Payment Schedule Number of Months', format1)
        sheet.write(6, 26, 'Payment Schedule Escalation', format1)
        sheet.write(6, 27, 'Payment Schedule Monthly Amount', format1)
        sheet.write(6, 28, 'Payment Schedule Total Amount', format1)
        sheet.write(6, 29, 'Payment Schedule Comment', format1)
        sheet.write(6, 30, 'Payment Schedule Invoice', format1)
        sheet.write(6, 31, 'Payment Schedule Invoice Status', format1)
        sheet.write(6, 32, 'Payment Schedule Refunded', format1)
        sheet.write(6, 33, 'Payment Schedule Payment Methods', format1)
        sheet.write(6, 34, 'Payment Schedule Overlapped	Status', format1)
        sheet.write(6, 35, 'Candidate', format1)
        sheet.write(6, 36, 'SAQ Vendor', format1)
       
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7
       
        domain = domain1 = location_name = ''
        in_qty = out_qty = 0
        
        domain = [('date','<=',data['date_from'])]
        
        
     
        
        purchase_subscritpion_ids = self.env['purchase.subscription'].search([('allow_lease','=',True)])
        schedule_lines = self.env['purchase.subscription.schedule']
        project_id = self.env['project.project']
        
        for sub in purchase_subscritpion_ids:
            #schedule_lines = self.env['purchase.subscription'].search([('purchase_subscription_id','=',sub.id),('date_from','>=',data['date_from']),('date_to','<=',data['date_from'])])
            for line in sub.purchase_subscription_schedule_line.filtered(lambda x: str(x.date_from) >= data['date_from'] and str(x.date_to) <= data['date_to']):
            #for line in schedule_lines:
                sheet.write(row, 0, sub.name, format2)
                sheet.write(row, 1, sub.date_start.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 2, sub.date.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 3, sub.project_id.name, format2)
                sheet.write(row, 4, sub.project_id.state_id.name, format2)
                sheet.write(row, 5, sub.partner_id.name, format2)
                sheet.write(row, 6, sub.partner_id.street_name, format2)
                sheet.write(row, 7, sub.partner_id.phone, format2)
                sheet.write(row, 8, sub.partner_id.mobile, format2)
                sheet.write(row, 9, sub.lease_hunter_partner_id.name, format2)
                sheet.write(row, 10, sub.product_id.name, format2)
                sheet.write(row, 11, sub.analytic_account_id.name, format2)
                sheet.write(row, 12, sub.allow_registration, format2)
                sheet.write(row, 13, sub.date_registration, format2)
                sheet.write(row, 14, sub.allow_stamp_duty, format2)
                sheet.write(row, 15, sub.date_stamp_duty, format2)
                sheet.write(row, 16, sub.amount_lease_original, format2)
                sheet.write(row, 17, sub.amount_lease_current, format2)
                sheet.write(row, 18, sub.amount_lease_total, format2)
                sheet.write(row, 19, sub.recurring_billed_total, format2)
                sheet.write(row, 20, sub.recurring_paid_total, format2)
                sheet.write(row, 21, (sub.amount_lease_total - sub.recurring_paid_total), format2)
                sheet.write(row, 22, sub.currency_id.name, format2)
                sheet.write(row, 23, line.date_from.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 24, line.date_to.strftime("%d/%m/%Y"), format2)
                sheet.write(row, 25, line.recurring_intervals, format2)
                sheet.write(row, 26, line.escalation, format2)
                sheet.write(row, 27, line.recurring_monthly_total, format2)
                sheet.write(row, 28, line.recurring_total, format2)
                sheet.write(row, 29, line.schedule_note, format2)
                sheet.write(row, 30, line.invoice_id.name, format2)
                sheet.write(row, 31, line.invoice_id.state, format2)
                sheet.write(row, 32, line.is_refunded, format2)
                sheet.write(row, 33, line.payment_details, format2)
                sheet.write(row, 34, line.is_overlap, format2)
                sheet.write(row, 35, sub.candidate, format2)
                sheet.write(row, 36, sub.lease_saq_partner_id.name, format2)
                
                row = row + 1
        