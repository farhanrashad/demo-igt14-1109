import json
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_stock_move.report_stock_move'
    _description = 'Stock Move Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        in_date = data['in_date']
        record = self.env['report.stock.move.wizard'].browse(self.env.context.get('active_ids'))
        loc_id = record.location_ids
        in_date = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
        in_date = in_date.strftime("%d/%m/%Y")

        format0 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, })
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True, 'bg_color': 'yellow'})
        ###For SPMRF
        sheet = workbook.add_worksheet('Stock Move Report')
        sheet.merge_range('C2:E2', 'Stock Move Report', format0)
        sheet.write(1, 4, 'Stock Move Report', format0)
        sheet.write(3, 0, 'Report On', format0)
        sheet.write(3, 1, in_date, format0)

        sheet.write(6, 0, 'Site', format1)
        sheet.write(6, 1, 'Source', format1)
        sheet.write(6, 2, 'Destination', format1)
        sheet.write(6, 3, 'Shipment', format1)
        sheet.write(6, 4, 'Movement', format1)
        sheet.write(6, 5, 'MRF', format1)
        sheet.write(6, 6, 'SPMRF', format1)
        sheet.write(6, 7, 'Product', format1)
        sheet.write(6, 8, 'Movement Time', format1)
        sheet.write(6, 9, 'Movement Date', format1)
        sheet.write(6, 10, 'IGT Serial No.', format1)
        sheet.write(6, 11, 'OEM Serial No.', format1)
        sheet.write(6, 12, 'In Quantity', format1)
        sheet.write(6, 13, 'Out Quantity', format1)
        sheet.write(6, 14, 'Balance', format1)

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 7

        domain = domain1 = location_name = ''
        in_qty = out_qty = 0

        domain = [('date', '<=', data['in_date'])]

        if data['product_ids']:
            domain += [('product_id', 'in', data['product_ids'])]

        # if data['location_ids']:
        # domain += ['|',('location_id','in',data['location_ids']),('location_dest_id','in',data['location_ids'])]
        # location_ids = self.env['stock.location'].search([('id', 'in', data['location_ids'])])
        # for location in location_ids:
        # location_name += location.name + ','

        if data['categ_ids']:
            categ_products_ids = self.env['product.product'].search([('categ_id', 'in', data['categ_ids'])])
            product_ids = tuple([pro_id.id for pro_id in categ_products_ids])
            domain += [('product_id', 'in', product_ids)]

        move_line_ids = self.env['stock.move.line'].search(domain)
        project_id = self.env['project.project']
        location_id = location_dest_id = self.env['stock.location']
        mrf_order_id = spmrf_order_id = self.env['stock.transfer.order']
        for line in move_line_ids.filtered(
                lambda x: x.location_id.id in data['location_ids'] or x.location_dest_id.id in data['location_ids']):
            # for line in move_line_ids:
            if line.location_id.usage == 'internal':
                out_qty = line.qty_done
            elif line.location_dest_id.usage == 'internal':
                in_qty = line.qty_done

            if line.stock_transfer_order_line_id:
                project_id = line.stock_transfer_order_line_id.project_id
            elif line.stock_transfer_return_line_id:
                project_id = line.stock_transfer_return_line_id.project_id

            if line.stock_transfer_order_line_id:
                location_id = line.stock_transfer_order_line_id.location_src_id
                location_dest_id = line.stock_transfer_order_line_id.location_dest_id
            elif line.stock_transfer_return_line_id:
                location_id = line.stock_transfer_return_line_id.location_src_id
                location_dest_id = line.stock_transfer_return_line_id.location_dest_id

            if line.stock_transfer_order_line_id.stock_transfer_order_id.transfer_order_type_id.code == 'MRF':
                mrf_order_id = line.stock_transfer_order_line_id.stock_transfer_order_id
            elif line.stock_transfer_order_line_id.stock_transfer_order_id.transfer_order_type_id.code == 'SPF':
                spmrf_order_id = line.stock_transfer_order_line_id.stock_transfer_order_id
            sheet.write(row, 0, loc_id.name, format2)
            sheet.write(row, 1, line.location_id.name, format2)
            sheet.write(row, 2, line.location_dest_id.name, format2)
            sheet.write(row, 3, line.picking_id.name, format2)
            sheet.write(row, 4, line.display_name, format2)
            if mrf_order_id.id:
                sheet.write(row, 5, mrf_order_id.name, format2)
            if spmrf_order_id.id:
                sheet.write(row, 6, spmrf_order_id.name, format2)
            sheet.write(row, 7, line.product_id.name, format2)
            sheet.write(row, 8, line.date.strftime("%H:%M:%S"), format2)
            sheet.write(row, 9, line.date.strftime("%d/%m/%Y"), format2)
            if line.stock_transfer_return_line_id.igt_barcode:
                sheet.write(row, 10, line.stock_transfer_return_line_id.igt_barcode, format2)
            if line.stock_transfer_return_line_id.oem_barcode:
                sheet.write(row, 11, line.stock_transfer_return_line_id.oem_barcode, format2)
            sheet.write(row, 12, in_qty, format2)
            sheet.write(row, 13, out_qty, format2)
            sheet.write(row, 14, (in_qty - out_qty), format2)
            row = row + 1
