import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_requisition_line_report.mrf_spmrf_report_xlsx'
    _description = 'Stock Transfer Material Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        start_date = data['start_date']
        end_date = data['end_date']
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        start_date = start_date.strftime("%Y/%m/%d")
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        end_date = end_date.strftime("%Y/%m/%d")
        
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        ###For SPMRF
        sheet = workbook.add_worksheet('SPMRF Line Report')
        sheet.merge_range('C2:E2', 'SPMRF Line Report', format1)
        sheet.write(1, 4, 'SPMRF Line Report', format1)
        sheet.write(3, 0, 'Date From', format1)
        sheet.write(3, 1, start_date, format1)
        sheet.write(4, 0, 'Date To', format1)
        sheet.write(4, 1, end_date, format1)

        sheet.write(6, 0, 'GTN/GDN Number', format1)
        sheet.write(6, 1, 'GTN/GDN Creation Date', format1)
        sheet.write(6, 2, 'GTN/GDN Date of Transfer', format1)
        sheet.write(6, 3, 'GTN/GDN Amount', format1)
        sheet.write(6, 4, 'SPMRF', format1)
        sheet.write(6, 5, 'Requestor', format1)
        sheet.write(6, 6, 'SPMRF Type', format1)
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
        sheet.write(6, 22, 'Return QTY', format1)
        sheet.write(6, 23, 'Received QTY', format1)
        sheet.write(6, 24, 'SPMRF State', format1)
        ###For MRF
        sheet1 = workbook.add_worksheet('MRF Line Report')
        sheet1.merge_range('C2:E2', 'MRF Line Report', format1)
        sheet1.write(1, 4, 'MRF Line Report', format1)
        sheet1.write(3, 0, 'Date From', format1)
        sheet1.write(3, 1, start_date, format1)
        sheet1.write(4, 0, 'Date To', format1)
        sheet1.write(4, 1, end_date, format1)

        sheet1.write(6, 0, 'GTN/GDN Number', format1)
        sheet1.write(6, 1, 'GTN/GDN Creation Date', format1)
        sheet1.write(6, 2, 'GTN/GDN Date of Transfer', format1)
        sheet1.write(6, 3, 'GTN/GDN Amount', format1)
        sheet1.write(6, 4, 'MRF', format1)
        sheet1.write(6, 5, 'Requestor', format1)
        sheet1.write(6, 6, 'MRF Type', format1)
        sheet1.write(6, 7, 'Related PO', format1)
        sheet1.write(6, 8, 'Source', format1)
        sheet1.write(6, 9, 'Destination', format1)
        sheet1.write(6, 10, 'Contractor', format1)
        sheet1.write(6, 11, 'Create Date', format1)
        sheet1.write(6, 12, 'Pick Up Date', format1)
        sheet1.write(6, 13, 'Return Date', format1)
        sheet1.write(6, 14, 'Material Supplier', format1)
        sheet1.write(6, 15, 'Product', format1)
        sheet1.write(6, 16, 'Description', format1)
        sheet1.write(6, 17, 'Product Code', format1)
        sheet1.write(6, 18, 'Product Category', format1)
        sheet1.write(6, 19, 'Material Condition', format1)
        sheet1.write(6, 20, 'Required QTY', format1)
        sheet1.write(6, 21, 'Transferred QTY', format1)
        sheet1.write(6, 22, 'Return QTY', format1)
        sheet1.write(6, 23, 'Received QTY', format1)
        sheet1.write(6, 24, 'MRF State', format1)
        
        ##For Return Lines
        sheet2 = workbook.add_worksheet('Return Line Report')
        sheet2.merge_range('C2:E2', 'Return Line Report', format1)
        sheet2.write(1, 4, 'Return Line Report', format1)
        sheet2.write(3, 0, 'Date From', format1)
        sheet2.write(3, 1, start_date, format1)
        sheet2.write(4, 0, 'Date To', format1)
        sheet2.write(4, 1, end_date, format1)

        sheet2.write(6, 0, 'GTN/GDN Number', format1)
        sheet2.write(6, 1, 'GTN/GDN Creation Date', format1)
        sheet2.write(6, 2, 'GTN/GDN Date of Transfer', format1)
        sheet2.write(6, 3, 'GTN/GDN Amount', format1)
        sheet2.write(6, 4, 'MRF', format1)
        sheet2.write(6, 5, 'Requestor', format1)
        sheet2.write(6, 6, 'MRF Type', format1)
        sheet2.write(6, 7, 'Related PO', format1)
        sheet2.write(6, 8, 'Source', format1)
        sheet2.write(6, 9, 'Destination', format1)
        sheet2.write(6, 10, 'Contractor', format1)
        sheet2.write(6, 11, 'Create Date', format1)
        sheet2.write(6, 12, 'Pick Up Date', format1)
        sheet2.write(6, 13, 'Return Date', format1)
        sheet2.write(6, 14, 'Material Supplier', format1)
        sheet2.write(6, 15, 'Product', format1)
        sheet2.write(6, 16, 'Description', format1)
        sheet2.write(6, 17, 'Product Code', format1)
        sheet2.write(6, 18, 'Product Category', format1)
        sheet2.write(6, 19, 'Material Condition', format1)
        sheet2.write(6, 20, 'Required QTY', format1)
        sheet2.write(6, 21, 'Transferred QTY', format1)
        sheet2.write(6, 22, 'Return QTY', format1)
        sheet2.write(6, 23, 'Received QTY', format1)
        sheet2.write(6, 24, 'MRF State', format1)
        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7
        row1 = 7
        row2 = 7
        spmrf_order_ids = self.env['stock.transfer.order'].search([('date_order','>=',data['start_date']),('date_order','<=',data['end_date'])])
        
        
        for spmrf_order in spmrf_order_ids:
            if spmrf_order.transfer_order_type_id.name == 'Spare Part Request Form':
                
                sheet.set_column(row, 0, 50)
                sheet.set_column(row, 1, 25)
                sheet.set_column(row, 2, 20)
                sheet.set_column(row, 3, 20)
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
                
                if spmrf_order.name:
                    name = spmrf_order.name
                else:
                    name = None
                if spmrf_order.user_id:
                    requestor = spmrf_order.user_id.name
                else:
                    requestor = None
                if spmrf_order.transfer_order_category_id:
                    transfer_category = spmrf_order.transfer_order_category_id.name
                else:
                    transfer_category = None
                if spmrf_order.purchase_id:
                    po = spmrf_order.purchase_id.name
                else:
                    po = None
                if spmrf_order.location_src_id:
                    src = spmrf_order.location_src_id.name
                else:
                    src = None
                if spmrf_order.location_dest_id:
                    dest = spmrf_order.location_dest_id.name
                else:
                    dest = None
                if spmrf_order.partner_id:
                    partner = spmrf_order.partner_id.name
                else:
                    partner = None
                if spmrf_order.date_order:
                    create_date = spmrf_order.date_order
                    create_date = create_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    create_date = None
                if spmrf_order.date_delivered:
                    actual_date = spmrf_order.date_delivered
                    actual_date = actual_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    actual_date = None
                if spmrf_order.date_returned:
                    return_date = spmrf_order.date_returned
                    return_date = return_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    return_date = None

                if spmrf_order.stage_id:
                    stage = spmrf_order.stage_id.name
                else:
                    stage = None
                    
                if self.env['stock.picking'].search([('origin','=',spmrf_order.name)]):
                    deliveries = self.env['stock.picking'].search([('origin','=',spmrf_order.name)])[0]
                    if deliveries:
                        gtn_number = deliveries.name
                        if deliveries.scheduled_date:
                            gtn_creation_date =  deliveries.scheduled_date
                            gtn_creation_date = gtn_creation_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_creation_date = None
                        if deliveries.scheduled_date:
                            gtn_transfer_date =  deliveries.scheduled_date
                            gtn_transfer_date = gtn_transfer_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_transfer_date = None
                    else:
                        gtn_number = None
                        gtn_creation_date = None
                        gtn_transfer_date = None
                else:
                    gtn_number = None
                    gtn_creation_date = None
                    gtn_transfer_date = None
                
                for product in spmrf_order.stock_transfer_order_line:
                    if product.supplier_id:
                        supplier = product.supplier_id.name
                    else:
                        supplier = None
                    if product.product_id:
                        product_name = product.product_id.name
                    else:
                        product_name = None
                    if product.product_id.categ_id:
                        product_category = product.product_id.categ_id.name
                    else:
                        product_category = None
                    if product.name:
                        description = product.name
                    else:
                        description = None
                    if product.product_id.default_code:
                        reference = product.product_id.default_code
                    else:
                        reference = None
                    if product.product_uom_qty:
                        demanded_qty = product.product_uom_qty
                    else:
                        demanded_qty = None
                    if product.delivered_qty:
                        delivered_qty = product.delivered_qty
                    else:
                        delivered_qty = None
                    if self.env['stock.picking'].search([('origin','=',spmrf_order.name)]):
                        deliveries = self.env['stock.picking'].search([('origin','=',spmrf_order.name)])[0]
                        if deliveries:
                            for delivery_product_orders in deliveries.move_ids_without_package:
                                if delivery_product_orders.product_id.name == product.product_id.name:
                                    price_total = delivery_product_orders.price_total
                            if price_total:
                                pass
                            else:
                                price_total = None
                        else:
                            price_total = None
                    else:
                        price_total = None
                    sheet.write(row, 0, gtn_number, format2)
                    sheet.write(row, 1, gtn_creation_date, format2)
                    sheet.write(row, 2, gtn_transfer_date, format2)
                    sheet.write(row, 3, price_total, format2)
                    sheet.write(row, 4, name, format2)
                    sheet.write(row, 5, requestor, format2)
                    sheet.write(row, 6, transfer_category, format2)
                    sheet.write(row, 7, po, format2)
                    sheet.write(row, 8, src, format2)
                    sheet.write(row, 9, dest, format2)
                    sheet.write(row, 10, partner, format2)
                    sheet.write(row, 11, create_date, format2)
                    sheet.write(row, 12, actual_date, format2)
                    sheet.write(row, 13, return_date, format2)
                    sheet.write(row, 14, supplier, format2)
                    sheet.write(row, 15, product_name, format2)
                    sheet.write(row, 16, description, format2)
                    sheet.write(row, 17, reference, format2)
                    sheet.write(row, 18, product_category, format2)
                    #sheet.write(row, 19, product_category, format2)            
                    sheet.write(row, 20, demanded_qty, format2)
                    sheet.write(row, 21, delivered_qty, format2)
                    #sheet.write(row, 22, return_qty, format2)
                    #sheet.write(row, 23, received_qty, format2)
                    sheet.write(row, 24, stage, format2)

                    row = row + 1
                    
            if spmrf_order.transfer_order_type_id.name == 'Spare Part Request Form':
                ######For Return Lines
                sheet2.set_column(row2, 0, 50)
                sheet2.set_column(row2, 1, 25)
                sheet2.set_column(row2, 2, 20)
                sheet2.set_column(row2, 3, 20)
                sheet2.set_column(row2, 4, 20)
                sheet2.set_column(row2, 5, 20)
                sheet2.set_column(row2, 6, 20)
                sheet2.set_column(row2, 7, 20)
                sheet2.set_column(row2, 8, 20)
                sheet2.set_column(row2, 9, 20)
                sheet2.set_column(row2, 10, 20)
                sheet2.set_column(row2, 11, 20)
                sheet2.set_column(row2, 12, 20)
                sheet2.set_column(row2, 13, 20)
                sheet2.set_column(row2, 14, 20)
                sheet2.set_column(row2, 15, 20)
                sheet2.set_column(row2, 16, 20)
                sheet2.set_column(row2, 17, 20)
                sheet2.set_column(row2, 18, 20)
                sheet2.set_column(row2, 19, 20)
                sheet2.set_column(row2, 20, 20)
                sheet2.set_column(row2, 21, 20)
                sheet2.set_column(row2, 22, 20)
                sheet2.set_column(row2, 23, 20)
                sheet2.set_column(row2, 24, 20)
                
                if spmrf_order.name:
                    name = spmrf_order.name
                else:
                    name = None
                if spmrf_order.user_id:
                    requestor = spmrf_order.user_id.name
                else:
                    requestor = None
                if spmrf_order.transfer_order_category_id:
                    transfer_category = spmrf_order.transfer_order_category_id.name
                else:
                    transfer_category = None
                if spmrf_order.purchase_id:
                    po = spmrf_order.purchase_id.name
                else:
                    po = None
                if spmrf_order.location_src_id:
                    src = spmrf_order.location_src_id.name
                else:
                    src = None
                if spmrf_order.location_dest_id:
                    dest = spmrf_order.location_dest_id.name
                else:
                    dest = None
                if spmrf_order.partner_id:
                    partner = spmrf_order.partner_id.name
                else:
                    partner = None
                if spmrf_order.date_order:
                    create_date = spmrf_order.date_order
                    create_date = create_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    create_date = None
                if spmrf_order.date_delivered:
                    actual_date = spmrf_order.date_delivered
                    actual_date = actual_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    actual_date = None
                if spmrf_order.date_returned:
                    return_date = spmrf_order.date_returned
                    return_date = return_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    return_date = None

                if spmrf_order.stage_id:
                    stage = spmrf_order.stage_id.name
                else:
                    stage = None
                    
                if self.env['stock.picking'].search([('origin','=',spmrf_order.name)]):
                    deliveries = self.env['stock.picking'].search([('origin','=',spmrf_order.name)])[0]
                    if deliveries:
                        gtn_number = deliveries.name
                        if deliveries.scheduled_date:
                            gtn_creation_date =  deliveries.scheduled_date
                            gtn_creation_date = gtn_creation_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_creation_date = None
                        if deliveries.scheduled_date:
                            gtn_transfer_date =  deliveries.scheduled_date
                            gtn_transfer_date = gtn_transfer_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_transfer_date = None
                    else:
                        gtn_number = None
                        gtn_creation_date = None
                        gtn_transfer_date = None
                else:
                    gtn_number = None
                    gtn_creation_date = None
                    gtn_transfer_date = None
                for return_product in spmrf_order.stock_transfer_return_line:
                    if return_product:
                        if return_product.product_uom_qty:
                            return_qty = return_product.product_uom_qty
                        else:
                            return_qty = None
                        if return_product.received_qty:
                            received_qty = return_product.received_qty
                        else:
                            received_qty = None
                        if return_product.supplier_id:
                            supplier = return_product.supplier_id.name
                        else:
                            supplier = None
                        if return_product.product_id:
                            product_name = return_product.product_id.name
                        else:
                            product_name = None
                        if return_product.product_id.categ_id:
                            product_category = return_product.product_id.categ_id.name
                        else:
                            product_category = None
                        if return_product.name:
                            description = return_product.name
                        else:
                            description = None
                        if return_product.product_id.default_code:
                            reference = return_product.product_id.default_code
                        else:
                            reference = None
                        if return_product.product_uom_qty:
                            demanded_qty = return_product.product_uom_qty
                        else:
                            demanded_qty = None
                        try:
                            if return_product.delivered_qty:
                                delivered_qty = return_product.delivered_qty
                            else:
                                delivered_qty = None
                        except:
                            delivered_qty = None

                        sheet2.write(row2, 0, gtn_number, format2)
                        sheet2.write(row2, 1, gtn_creation_date, format2)
                        sheet2.write(row2, 2, gtn_transfer_date, format2)
                        sheet2.write(row2, 3, price_total, format2)
                        sheet2.write(row2, 4, name, format2)
                        sheet2.write(row2, 5, requestor, format2)
                        sheet2.write(row2, 6, transfer_category, format2)
                        sheet2.write(row2, 7, po, format2)
                        sheet2.write(row2, 8, src, format2)
                        sheet2.write(row2, 9, dest, format2)
                        sheet2.write(row2, 10, partner, format2)
                        sheet2.write(row2, 11, create_date, format2)
                        sheet2.write(row2, 12, actual_date, format2)
                        sheet2.write(row2, 13, return_date, format2)
                        sheet2.write(row2, 14, supplier, format2)
                        sheet2.write(row2, 15, product_name, format2)
                        sheet2.write(row2, 16, description, format2)
                        sheet2.write(row2, 17, reference, format2)
                        sheet2.write(row2, 18, product_category, format2)
                        #sheet2.write(row2, 19, product_category, format2)            
                        sheet2.write(row2, 20, demanded_qty, format2)
                        sheet2.write(row2, 21, delivered_qty, format2)
                        sheet2.write(row2, 22, return_qty, format2)
                        sheet2.write(row2, 23, received_qty, format2)
                        sheet2.write(row2, 24, stage, format2)

                        row2 = row2 + 1
                
            elif spmrf_order.transfer_order_type_id.name == 'Material Request Form':

                sheet1.set_column(row1, 0, 50)
                sheet1.set_column(row1, 1, 25)
                sheet1.set_column(row1, 2, 20)
                sheet1.set_column(row1, 3, 20)
                sheet1.set_column(row1, 4, 20)
                sheet1.set_column(row1, 5, 20)
                sheet1.set_column(row1, 6, 20)
                sheet1.set_column(row1, 7, 20)
                sheet1.set_column(row1, 8, 20)
                sheet1.set_column(row1, 9, 20)
                sheet1.set_column(row1, 10, 20)
                sheet1.set_column(row1, 11, 20)
                sheet1.set_column(row1, 12, 20)
                sheet1.set_column(row1, 13, 20)
                sheet1.set_column(row1, 14, 20)
                sheet1.set_column(row1, 15, 20)
                sheet1.set_column(row1, 16, 20)
                sheet1.set_column(row1, 17, 20)
                sheet1.set_column(row1, 18, 20)
                sheet1.set_column(row1, 19, 20)
                sheet1.set_column(row1, 20, 20)
                sheet1.set_column(row1, 21, 20)
                sheet1.set_column(row1, 22, 20)
                sheet1.set_column(row1, 23, 20)
                sheet1.set_column(row1, 24, 20)
                
                if spmrf_order.name:
                    name = spmrf_order.name
                else:
                    name = None
                if spmrf_order.user_id:
                    requestor = spmrf_order.user_id.name
                else:
                    requestor = None
                if spmrf_order.transfer_order_category_id:
                    transfer_category = spmrf_order.transfer_order_category_id.name
                else:
                    transfer_category = None
                if spmrf_order.purchase_id:
                    po = spmrf_order.purchase_id.name
                else:
                    po = None
                if spmrf_order.location_src_id:
                    src = spmrf_order.location_src_id.name
                else:
                    src = None
                if spmrf_order.location_dest_id:
                    dest = spmrf_order.location_dest_id.name
                else:
                    dest = None
                if spmrf_order.partner_id:
                    partner = spmrf_order.partner_id.name
                else:
                    partner = None
                if spmrf_order.date_order:
                    create_date = spmrf_order.date_order
                    create_date = create_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    create_date = None
                if spmrf_order.date_delivered:
                    actual_date = spmrf_order.date_delivered
                    actual_date = actual_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    actual_date = None
                if spmrf_order.date_returned:
                    return_date = spmrf_order.date_returned
                    return_date = return_date.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    return_date = None

                if spmrf_order.stage_id:
                    stage = spmrf_order.stage_id.name
                else:
                    stage = None
                
                if self.env['stock.picking'].search([('origin','=',spmrf_order.name)]):
                    deliveries = self.env['stock.picking'].search([('origin','=',spmrf_order.name)])[0]
                    if deliveries:
                        gtn_number = deliveries.name
                        if deliveries.scheduled_date:
                            gtn_creation_date =  deliveries.scheduled_date
                            gtn_creation_date = gtn_creation_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_creation_date = None
                        if deliveries.scheduled_date:
                            gtn_transfer_date =  deliveries.scheduled_date
                            gtn_transfer_date = gtn_transfer_date.strftime("%Y/%m/%d %H:%M:%S")
                        else:
                            gtn_transfer_date = None
                    else:
                        gtn_number = None
                        gtn_creation_date = None
                        gtn_transfer_date = None
                else:
                    gtn_number = None
                    gtn_creation_date = None
                    gtn_transfer_date = None
                for product in spmrf_order.stock_transfer_order_line:
                    if product.supplier_id:
                        supplier = product.supplier_id.name
                    else:
                        supplier = None
                    if product.product_id:
                        product_name = product.product_id.name
                    else:
                        product_name = None
                    if product.product_id.categ_id:
                        product_category = product.product_id.categ_id.name
                    else:
                        product_category = None
                    if product.name:
                        description = product.name
                    else:
                        description = None
                    if product.product_id.default_code:
                        reference = product.product_id.default_code
                    else:
                        reference = None
                    if product.product_uom_qty:
                        demanded_qty = product.product_uom_qty
                    else:
                        demanded_qty = None
                    if product.delivered_qty:
                        delivered_qty = product.delivered_qty
                    else:
                        delivered_qty = None
                    if self.env['stock.picking'].search([('origin','=',spmrf_order.name)]):
                        deliveries = self.env['stock.picking'].search([('origin','=',spmrf_order.name)])[0]
                        if deliveries:
                            for delivery_product_orders in deliveries.move_ids_without_package:
                                if delivery_product_orders.product_id.name == product.product_id.name:
                                    price_total = delivery_product_orders.price_total
                            if price_total:
                                pass
                            else:
                                price_total = None
                        else:
                            price_total = None
                    else:
                        price_total = None
                    sheet1.write(row1, 0, gtn_number, format2)
                    sheet1.write(row1, 1, gtn_creation_date, format2)
                    sheet1.write(row1, 2, gtn_transfer_date, format2)
                    sheet1.write(row1, 3, price_total, format2)
                    sheet1.write(row1, 4, name, format2)
                    sheet1.write(row1, 5, requestor, format2)
                    sheet1.write(row1, 6, transfer_category, format2)
                    sheet1.write(row1, 7, po, format2)
                    sheet1.write(row1, 8, src, format2)
                    sheet1.write(row1, 9, dest, format2)
                    sheet1.write(row1, 10, partner, format2)
                    sheet1.write(row1, 11, create_date, format2)
                    sheet1.write(row1, 12, actual_date, format2)
                    sheet1.write(row1, 13, return_date, format2)
                    sheet1.write(row1, 14, supplier, format2)
                    sheet1.write(row1, 15, product_name, format2)
                    sheet1.write(row1, 16, description, format2)
                    sheet1.write(row1, 17, reference, format2)
                    sheet1.write(row1, 18, product_category, format2)
                    #sheet1.write(row1, 19, product_category, format2)            
                    sheet1.write(row1, 20, demanded_qty, format2)
                    sheet1.write(row1, 21, delivered_qty, format2)
                    #sheet1.write(row1, 22, return_qty, format2)
                    #sheet1.write(row1, 23, received_qty, format2)
                    sheet1.write(row1, 24, stage, format2)

                    row1 = row1 + 1
