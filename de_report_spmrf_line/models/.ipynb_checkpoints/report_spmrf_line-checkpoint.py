import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_spmrf_line.report_spmrf_line'
    _description = 'SPMRF Line Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        from_date = data['from_date']
        from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        from_date = from_date.strftime("%d/%m/%Y")
        
        to_date = data['to_date']
        to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime("%d/%m/%Y")
        
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        #For SPMRF
        sheet = workbook.add_worksheet('SPMRF Line Report')
        sheet.merge_range('C2:E2', 'SPMRF Line Report', format0)
        sheet.write(3, 0, 'From Date', format0)
        sheet.write(3, 1, from_date, format0)
        sheet.write(4, 0, 'To Date', format0)
        sheet.write(4, 1, to_date, format0)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7
        
        sheet.write(6, 0, 'SPMRF', format1)
        sheet.write(6, 1, 'Requestor', format1)
        sheet.write(6, 2, 'SPMRF Type', format1)
        sheet.write(6, 3, 'Related PO', format1)
        sheet.write(6, 4, 'Source', format1)
        sheet.write(6, 5, 'Destination', format1)
        sheet.write(6, 6, 'Contractor', format1)
        sheet.write(6, 7, 'Create Date', format1)
        sheet.write(6, 8, 'Pick Up Date', format1)
        sheet.write(6, 9, 'Return Date', format1)
        sheet.write(6, 10, 'Material Supplier', format1)
        sheet.write(6, 11, 'Product', format1)
        sheet.write(6, 12, 'Description', format1)
        sheet.write(6, 13, 'Product Code', format1)
        sheet.write(6, 14, 'Product Category', format1)
        sheet.write(6, 15, 'Material Condition', format1)
        sheet.write(6, 16, 'Required QTY', format1)
        sheet.write(6, 17, 'Transferred QTY', format1)
        sheet.write(6, 18, 'Return QTY', format1)
        sheet.write(6, 19, 'Received QTY', format1)
        sheet.write(6, 20, 'SPMRF State', format1)
        sheet.write(6, 21, 'Related SPMRF', format1)
        sheet.write(6, 22, 'Previous Stage', format1)
        
        domain = domain1 = location_name = ''
        
        products_list = []
        domain = [('date_order','>=',data['from_date'])]
        domain += [('date_order','<=',data['to_date'])]
        
        if data['product_ids']:
            domain += [('product_id','in',data['product_ids'])]
            
        if data['categ_ids']:
            categ_products_ids = self.env['product.product'].search([('categ_id', 'in', data['categ_ids'])])
            product_ids = tuple([pro_id.id for pro_id in categ_products_ids])
            domain += [('product_id','in',product_ids)]
            
        transfer_order_ids = self.env['stock.transfer.order'].search(domain)
        picking_id = self.env['stock.picking']
        
        return_lines = self.env['stock.transfer.return.line']
        return_qty = received_qty = 0
        
        for order in transfer_order_ids.filtered(lambda r: r.transfer_order_type_id.code == 'SPF'):
            picking_id = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id)],limit=1)
            return_lines = self.env['stock.transfer.return.line'].search([('stock_transfer_order_id','=',order.id)])
            return_qty = received_qty = 0
            
            for rline in return_lines:
                return_qty += rline.product_uom_qty
                received_qty += rline.received_qty
                
            for line in order.stock_transfer_order_line:
                sheet.set_column(row, 0, 50)
                sheet.set_column(row, 1, 25)
                sheet.set_column(row, 2, 20)
                #sheet.set_column(row, 3, 20)
                sheet.set_column(row, 4, 20)
                sheet.set_column(row, 5, 20)
                sheet.set_column(row, 6, 20)
                sheet.set_column(row, 7, 20)
                sheet.set_column(row, 8, 20)
                sheet.set_column(row, 9, 20)
                sheet.set_column(row, 10, 20)
                sheet.set_column(row, 11, 20)
                sheet.set_column(row, 12, 20)
                sheet.set_column(row, 13, 20)
                sheet.set_column(row, 14, 20)
                sheet.set_column(row, 15, 20)
                sheet.set_column(row, 16, 20)
                sheet.set_column(row, 17, 20)
                sheet.set_column(row, 18, 20)
                sheet.set_column(row, 19, 20)
                sheet.set_column(row, 20, 20)
                sheet.set_column(row, 21, 20)
                sheet.set_column(row, 22, 20)
                sheet.set_column(row, 23, 20)
                sheet.set_column(row, 24, 20)
                
                #if picking_id:
                #    sheet.write(row, 0, picking_id.name, format2)
                   
                sheet.write(row, 0, order.name, format2)
                sheet.write(row, 1, order.user_id.name, format2)
                sheet.write(row, 2, order.transfer_order_category_id.name, format2)
                if order.purchase_id:
                    sheet.write(row, 3, order.purchase_id.name, format2)
                sheet.write(row, 4, order.location_src_id.name, format2)
                sheet.write(row, 5, line.location_dest_id.name, format2)
                sheet.write(row, 6, order.partner_id.name, format2)
                sheet.write(row, 7, order.date_order.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if order.delivery_deadline:
                    sheet.write(row, 8, order.delivery_deadline.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if order.order_deadline:
                    sheet.write(row, 9, order.order_deadline.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if line.supplier_id:
                    sheet.write(row, 10, line.supplier_id.name, format2)
                sheet.write(row, 11, line.product_id.name, format2)
                sheet.write(row, 12, line.name, format2)
                sheet.write(row, 13, line.product_id.default_code, format2)
                sheet.write(row, 14, line.product_id.categ_id.name, format2)
                #sheet.write(row, 15, product_category, format2)            
                sheet.write(row, 16, line.product_uom_qty, format2)
                sheet.write(row, 17, line.delivered_qty, format2)
                sheet.write(row, 18, return_qty, format2)
                sheet.write(row, 19, received_qty, format2)
                sheet.write(row, 20, order.stage_id.name, format2)
                if order.stock_transfer_order_id.id:
                    sheet.write(row, 21, order.stock_transfer_order_id.name, format2)
                if order.last_stage_id.id:
                    sheet.write(row, 22, order.last_stage_id.name, format2)

                row = row + 1
                
        #For Return
        sheet = workbook.add_worksheet('Return Line Report')
        sheet.merge_range('C2:E2', 'Return Line Report', format0)
        sheet.write(3, 0, 'From Date', format0)
        sheet.write(3, 1, from_date, format0)
        sheet.write(4, 0, 'To Date', format0)
        sheet.write(4, 1, to_date, format0)
        
        row = 7
        
        sheet.write(6, 0, 'GTN/GDN Number', format1)
        sheet.write(6, 1, 'GTN/GDN Creation Date', format1)
        sheet.write(6, 2, 'GTN/GDN Date of Transfer', format1)
        #sheet.write(6, 3, 'GTN/GDN Amount', format1)
        sheet.write(6, 4, 'MRF', format1)
        sheet.write(6, 5, 'Requestor', format1)
        sheet.write(6, 6, 'MRF Type', format1)
        sheet.write(6, 7, 'Related PO', format1)
        sheet.write(6, 8, 'Source', format1)
        sheet.write(6, 9, 'Destination', format1)
        sheet.write(6, 10, 'Contractor', format1)
        sheet.write(6, 11, 'Create Date', format1)
        sheet.write(6, 12, 'Pick Up Date', format1)
        sheet.write(6, 13, 'Return Date', format1)
        sheet.write(6, 14, 'Material Supplier', format1)
        sheet.write(6, 15, 'Product', format1)
        sheet.write(6, 16, 'Description', format1)
        sheet.write(6, 17, 'Product Code', format1)
        sheet.write(6, 18, 'Product Category', format1)
        sheet.write(6, 19, 'Material Condition', format1)
        sheet.write(6, 20, 'Required QTY', format1)
        sheet.write(6, 21, 'Transferred QTY', format1)
        sheet.write(6, 22, 'Return State', format1)
        
        for order in transfer_order_ids.filtered(lambda r: r.transfer_order_type_id.code == 'SPF'):
            picking_id = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id),('picking_type_id','=',order.picking_type_id.return_picking_type_id.id)],limit=1)
            return_lines = self.env['stock.transfer.return.line'].search([('stock_transfer_order_id','=',order.id)])
            return_qty = received_qty = 0
                
            for line in order.stock_transfer_return_line:
                sheet.set_column(row, 0, 50)
                sheet.set_column(row, 1, 25)
                sheet.set_column(row, 2, 20)
                #sheet.set_column(row, 3, 20)
                sheet.set_column(row, 4, 20)
                sheet.set_column(row, 5, 20)
                sheet.set_column(row, 6, 20)
                sheet.set_column(row, 7, 20)
                sheet.set_column(row, 8, 20)
                sheet.set_column(row, 9, 20)
                sheet.set_column(row, 10, 20)
                sheet.set_column(row, 11, 20)
                sheet.set_column(row, 12, 20)
                sheet.set_column(row, 13, 20)
                sheet.set_column(row, 14, 20)
                sheet.set_column(row, 15, 20)
                sheet.set_column(row, 16, 20)
                sheet.set_column(row, 17, 20)
                sheet.set_column(row, 18, 20)
                sheet.set_column(row, 19, 20)
                sheet.set_column(row, 20, 20)
                sheet.set_column(row, 21, 20)
                sheet.set_column(row, 22, 20)
                
                if picking_id:
                    sheet.write(row, 0, picking_id.name, format2)
                    sheet.write(row, 1, picking_id.create_date.strftime("%Y/%m/%d %H:%M:%S"), format2)
                    sheet.write(row, 2, picking_id.scheduled_date.strftime("%Y/%m/%d %H:%M:%S"), format2)
                    #sheet.write(row, 3, picking_id.total_base_signed, format2)
                    sheet.write(row, 8, picking_id.location_id.name, format2)
                    sheet.write(row, 9, picking_id.location_dest_id.name, format2)
                sheet.write(row, 4, order.name, format2)
                sheet.write(row, 5, order.user_id.name, format2)
                sheet.write(row, 6, order.transfer_order_category_id.name, format2)
                if order.purchase_id:
                    sheet.write(row, 7, order.purchase_id.name, format2)
                sheet.write(row, 10, order.partner_id.name, format2)
                sheet.write(row, 11, order.date_order.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if order.date_delivered:
                    sheet.write(row, 12, order.date_delivered.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if order.date_returned:
                    sheet.write(row, 13, order.date_returned.strftime("%Y/%m/%d %H:%M:%S"), format2)
                if line.supplier_id:
                    sheet.write(row, 14, line.supplier_id.name, format2)
                sheet.write(row, 15, line.product_id.name, format2)
                sheet.write(row, 16, line.name, format2)
                sheet.write(row, 17, line.product_id.default_code, format2)
                sheet.write(row, 18, line.product_id.categ_id.name, format2)
                #sheet.write(row, 19, product_category, format2)            
                sheet.write(row, 20, line.product_uom_qty, format2)
                sheet.write(row, 21, line.received_qty, format2)
                sheet.write(row, 22, order.stage_id.name, format2)
                row = row + 1
        
        