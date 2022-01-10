import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_inventory_availability.xlsx'
    _description = 'Inventory Availability Report Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        in_date = data['in_date']
        in_date = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
        in_date = in_date.strftime("%d/%m/%Y")
        
        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True,})
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Product Availability')
        sheet.merge_range('C2:E2', 'Product Availability', format0)
        sheet.write(1, 4, 'Product Availability', format0)
        sheet.write(3, 0, 'Report On', format0)
        sheet.write(3, 1, in_date, format0)

        sheet.write(6, 0, 'Product Cateegory', format1)
        sheet.write(6, 1, 'Product', format1)
        sheet.write(6, 2, 'Product Code', format1)
        sheet.write(6, 3, 'UOM', format1)
        sheet.write(6, 4, 'Inhand Qty', format1)
        sheet.write(6, 5, 'Reserved Qty', format1)
        sheet.write(6, 6, 'MRF Reserved Qty', format1)
        sheet.write(6, 7, 'SPMRF Reserved Qty', format1)
        sheet.write(6, 8, 'Available Qty', format1)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7
       
        domain = domain1 = domain_mrf = domain_spmrf = ''
        
        products_list = []
        domain = [('in_date','<=',data['in_date'])]
        if data['product_ids']:
            domain += [('product_id','in',data['product_ids'])]
        if data['location_ids']:            
            domain += [('location_id','in',data['location_ids'])]
            
        if data['categ_ids']:
            categ_products_ids = self.env['product.product'].search([('categ_id', 'in', data['categ_ids'])])
            product_ids = tuple([pro_id.id for pro_id in categ_products_ids])
            domain += [('product_id','in',product_ids)]
        
        quant_product_ids = self.env['stock.quant'].search(domain)
        for p in quant_product_ids.product_id:
            if p not in products_list:
                products_list.append(p)
        
        quantity = stock_value = avail_qty = reserved_qty = reserved_mrf = reserved_spmrf = 0
        pickings = self.env['stock.picking']
        for product in products_list:
            quantity = stock_value = avail_qty = reserved_qty = reserved_mrf = reserved_spmrf = 0
            domain1 = domain + [('product_id','=',product.id)]
            
            quant_ids = self.env['stock.quant'].search(domain1)
            for quant in quant_ids:
                quantity += quant.quantity
                stock_value += quant.value
                avail_qty += quant.available_quantity
                reserved_qty = quantity - avail_qty
            
            sheet.write(row, 0, product.categ_id.name, format2)
            sheet.write(row, 1, product.name, format2)
            sheet.write(row, 2, product.default_code, format2)
            sheet.write(row, 3, product.uom_id.name, format2)
            sheet.write(row, 4, quantity, format2)
            
            pickings = self.env['stock.picking'].search([('stock_transfer_order_id','!=',False),('state','not in',['done','cancel']),('scheduled_date','<=',data['in_date'])])
            
            order_line_ids = self.env['stock.transfer.order.line'].search([('stage_category','in',['progress'])])

            if pickings:
                for picking in pickings:
                    for line in picking.move_lines.filtered(lambda x: x.product_id.id == product.id):
                        if picking.stock_transfer_order_id.transfer_order_type_id.code == 'MRF' and picking.picking_type_id.id == picking.stock_transfer_order_id.picking_type_id.id:
                            reserved_mrf += line.product_uom_qty
                        elif picking.stock_transfer_order_id.transfer_order_type_id.code == 'SPF' and picking.picking_type_id.id == picking.stock_transfer_order_id.picking_type_id.id:
                            reserved_spmrf += line.product_uom_qty
            
            for line in order_line_ids.filtered(lambda x: x.product_id.id == product.id):
                if line.stock_transfer_order_id.transfer_order_type_id.code == 'MRF':
                    reserved_mrf += line.product_uom_qty
                elif line.stock_transfer_order_id.transfer_order_type_id.code == 'SPF':
                    reserved_spmrf += line.product_uom_qty
                    
            sheet.write(row, 5, (reserved_mrf+reserved_spmrf), format2)
            sheet.write(row, 6, reserved_mrf, format2)
            sheet.write(row, 7, reserved_spmrf, format2)
            sheet.write(row, 8, (quantity-(reserved_mrf+reserved_spmrf)), format2)
            row = row + 1
            
                
            
                #domain_mrf = [('product_id','=',product.id),('transfer_order_type_code','=','MRF'),('state','in',['assigned','partially_available'])]
                #domain_spmrf = [('product_id','=',product.id),('transfer_order_type_code','=','SPMRF'),('state','in',['assigned','partially_available'])]
            
                #mrf_move_line_ids = self.env['stock.move.line'].search(domain_mrf)
                #for line in mrf_move_line_ids:
                #    reserved_mrf += line.product_uom_qty
            
                #spmrf_move_line_ids = self.env['stock.move.line'].search(domain_spmrf)
                #for line in spmrf_move_line_ids:
                #    reserved_spmrf += line.product_uom_qty
            
            
        