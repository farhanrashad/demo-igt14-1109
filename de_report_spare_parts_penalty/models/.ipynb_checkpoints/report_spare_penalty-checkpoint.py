import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_spare_penalty.report_spare_penalty'
    _description = 'Spare Penalty Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        in_date = data['in_date']
        in_date = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
        in_date = in_date.strftime("%d/%m/%Y")
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Spare Parts Penalty Report')
        sheet.merge_range('C2:E2', 'Spare Parts Penalty Report', format0)
        sheet.write(1, 4, 'Spare Parts Penalty Report', format0)
        sheet.write(3, 0, 'Report On', format0)
        sheet.write(3, 1, in_date, format0)
    
        sheet.write(6, 0, 'MRF Number', format1)
        sheet.write(6, 1, 'MRF Type', format1)
        sheet.write(6, 2, 'Requestor', format1)
        sheet.write(6, 3, 'Supplier', format1)
        sheet.write(6, 4, 'Submission Date', format1)
        sheet.write(6, 5, 'Pickup Date', format1)
        sheet.write(6, 6, 'Penalty Effective Date', format1)
        sheet.write(6, 7, 'Creation Date', format1)
        sheet.write(6, 8, 'Site', format1)
        sheet.write(6, 9, 'On Air', format1)
        sheet.write(6, 10, 'Asset', format1)
        sheet.write(6, 11, 'Product Code', format1)
        sheet.write(6, 12, 'Lifetime', format1)
        sheet.write(6, 13, 'Used Life', format1)
        sheet.write(6, 14, 'Remaining Life', format1)
        sheet.write(6, 15, 'Deliver', format1)
        sheet.write(6, 16, 'Return', format1)
        sheet.write(6, 17, 'Quantity', format1)
        sheet.write(6, 18, 'Product Cost', format1)
        sheet.write(6, 19, 'Penalty', format1)
        sheet.write(6, 20, 'Backcharged', format1)
        sheet.write(6, 21, 'Total', format1)
        sheet.write(6, 22, 'Returned', format1)
        sheet.write(6, 23, 'Remakrs', format1)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7
       
        domain = domain1 = location_name = ''
        in_qty = out_qty = 0
        
        domain = [('date_order','<=',data['in_date'])]
        
        if data['product_ids']:
            domain += [('product_id','in',data['product_ids'])]
        
        
        #if data['location_ids']:            
            #domain += ['|',('location_id','in',data['location_ids']),('location_dest_id','in',data['location_ids'])]
            #location_ids = self.env['stock.location'].search([('id', 'in', data['location_ids'])])
            #for location in location_ids:
                #location_name += location.name + ','
            
        if data['categ_ids']:
            categ_products_ids = self.env['product.product'].search([('categ_id', 'in', data['categ_ids'])])
            product_ids = tuple([pro_id.id for pro_id in categ_products_ids])
            domain += [('product_id','in',product_ids)]
     
        
        transfer_order_line_ids = self.env['stock.transfer.order.line'].search(domain)
        project_id = self.env['project.project']
        location_id = location_dest_id = self.env['stock.location']
        mrf_order_id = spmrf_order_id = self.env['stock.transfer.order']
        
        
        for line in transfer_order_line_ids.filtered(lambda x: x.stock_transfer_order_id.code == 'MRF'):   
            sheet.write(row, 0, line.stock_transfer_order_id.name, format2)
            sheet.write(row, 1, line.transfer_order_category_id.name, format2)
            sheet.write(row, 2, line.user_id.name, format2)
            sheet.write(row, 3, line.supplier_id.name, format2)
            sheet.write(row, 4, line.stock_transfer_order_id.date_order, format2)
            sheet.write(row, 5, line.stock_transfer_order_id.date_delivered, format2)
            sheet.write(row, 6, '0', format2)
            sheet.write(row, 7, '0', format2)
            sheet.write(row, 8, line.project_id.name, format2)
            sheet.write(row, 9, '0', format2)
            sheet.write(row, 10, '0', format2)
            sheet.write(row, 11, line.product_id.default_code, format2)
            sheet.write(row, 12, '0', format2)
            sheet.write(row, 13, '0', format2)
            sheet.write(row, 14, '0', format2)
            sheet.write(row, 15, '0', format2)
            sheet.write(row, 16, line.delivered_qty, format2)
            sheet.write(row, 17, '0', format2)
            sheet.write(row, 18, line.product_uom_qty, format2)
            sheet.write(row, 19, line.product_id.standard_price, format2)
            sheet.write(row, 20, '0', format2)
            sheet.write(row, 21, '0', format2)
            sheet.write(row, 22, '0', format2)
            sheet.write(row, 23, '0', format2)
            sheet.write(row, 24, '0', format2)
                                
       
            row = row + 1
        