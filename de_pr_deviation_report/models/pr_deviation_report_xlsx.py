import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_pr_deviation_report.pr_deviation_report_xlsx'
    _description = 'Purchase Requisition Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines,model="ir.actions.report",output_format="xlsx",report_name="de_pr_deviation_report.pr_deviation_report_xlsx"):
        

        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('PR Deviation Report')
        sheet.write(3, 0, 'Order Reference', format1)
        sheet.write(3, 1, 'Old PR / Current PR', format1)
        sheet.write(3, 2, 'Product', format1)
        sheet.write(3, 3, 'User Name', format1)
        sheet.write(3, 4, 'Currency', format1)
        sheet.write(3, 5, 'Original PR Quantity', format1)
        sheet.write(3, 6, 'PR Updated Quantity', format1)
        sheet.write(3, 7, 'Total Deviation Quantity', format1)
        sheet.write(3, 8, 'Original PR Unit Price', format1)
        sheet.write(3, 9, 'PR Updated Unit Price', format1)
        sheet.write(3, 10, 'Total Deviation Unit Price', format1)
        sheet.write(3, 11, 'Original PR Amount', format1)
        sheet.write(3, 12, 'PR Updated Amount', format1)
        sheet.write(3, 13, 'Total Deviation Value', format1)
        sheet.write(3, 14, 'History Create Date', format1)
        sheet.write(3, 15, 'History Record', format1)
        sheet.write(3, 16, 'Reason', format1)

        
        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
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

        #purchase_order_ids = self.env['purchase.order'].browse(data['id'])

        for id in lines:
            try:
                if id.old_revision_ids:
                    if id.user_id:
                        username = id.user_id.name
                    else:
                        username = None
                    if id.currency_id:
                        currency = id.currency_id.name
                    else:
                        currency = None
                    try:
                        if id.reason:
                            reason = id.reason
                        else:
                            reason = None
                    except:
                        reason = None
                        # original_po_amount = None
                    if id.old_revision_ids:
                        for line in id.old_revision_ids[-1]:
                            name = line.name
                            history_create_date = line.create_date
                            if history_create_date:
                                history_create_date = history_create_date.strftime("%Y-%m-%d %H:%M:%S")
                                history_record = 'Yes'
                            else:
                                history_record = 'No'
                    if id.line_ids:
                        updated_po_amount = 0
                        updated_quantity = 0
                        updated_price = 0
                        for line in id.line_ids:
                            product = line.product_id.name
                            updated_quantity = line.product_qty
                            updated_price = line.price_unit
                            updated_po_amount  = line.price_total_base

                            purchase_req = self.env['purchase.requisition'].search([('product_id', '=', line.product_id.id),('name','=',name)])
                            po_amount = 0
                            quantity = 0
                            price = 0
                            if purchase_req:
                                for order in purchase_req:
                                    if order.line_ids:
                                        for line_model in order.line_ids:
                                            if line_model.product_id.id == line.product_id.id:
                                                quantity = line_model.product_qty
                                                price = line_model.price_unit
                                                po_amount  = line_model.price_total_base
                                                total_deviation_qty = updated_quantity - quantity
                                                total_deviation_price = updated_price - price
                                                total_deviation_amount = updated_po_amount - po_amount

                                                sheet.write(row, 0, name, format2)
                                                sheet.write(row, 1, id.name, format2)
                                                sheet.write(row, 2, product, format2)
                                                sheet.write(row, 3, username, format2)
                                                sheet.write(row, 4, currency, format2)
                                                sheet.write(row, 5, quantity, format2)
                                                sheet.write(row, 6, updated_quantity, format2)
                                                sheet.write(row, 7, total_deviation_qty, format2)
                                                sheet.write(row, 8, price, format2)
                                                sheet.write(row, 9, updated_price, format2)
                                                sheet.write(row, 10, total_deviation_price, format2)
                                                sheet.write(row, 11, po_amount, format2)
                                                sheet.write(row, 12, updated_po_amount, format2)
                                                sheet.write(row, 13, total_deviation_amount, format2)
                                                sheet.write(row, 14, history_create_date, format2)
                                                sheet.write(row, 15, history_record, format2)
                                                sheet.write(row, 16, reason, format2)

                                                row = row + 1
                                                break

                                            else:
                                                quantity = line_model.product_qty
                                                price = line.price_unit
                                                po_amount  = line.price_total_base
                                                total_deviation_qty = updated_quantity - quantity
                                                total_deviation_price = updated_price - price
                                                total_deviation_amount = updated_po_amount - po_amount

                                                sheet.write(row, 0, name, format2)
                                                sheet.write(row, 1, id.name, format2)
                                                sheet.write(row, 2, product, format2)
                                                sheet.write(row, 3, username, format2)
                                                sheet.write(row, 4, currency, format2)
                                                sheet.write(row, 5, quantity, format2)
                                                sheet.write(row, 6, updated_quantity, format2)
                                                sheet.write(row, 7, total_deviation_qty, format2)
                                                sheet.write(row, 8, price, format2)
                                                sheet.write(row, 9, updated_price, format2)
                                                sheet.write(row, 10, total_deviation_price, format2)
                                                sheet.write(row, 11, po_amount, format2)
                                                sheet.write(row, 12, updated_po_amount, format2)
                                                sheet.write(row, 13, total_deviation_amount, format2)
                                                sheet.write(row, 14, history_create_date, format2)
                                                sheet.write(row, 15, history_record, format2)
                                                sheet.write(row, 16, reason, format2)

                                                row = row + 1
                                                break


                            else:
                                total_deviation_qty = updated_quantity - quantity
                                total_deviation_price = updated_price - price
                                total_deviation_amount = updated_po_amount - po_amount

                                sheet.write(row, 0, name, format2)
                                sheet.write(row, 1, id.name, format2)
                                sheet.write(row, 2, product, format2)
                                sheet.write(row, 3, username, format2)
                                sheet.write(row, 4, currency, format2)
                                sheet.write(row, 5, quantity, format2)
                                sheet.write(row, 6, updated_quantity, format2)
                                sheet.write(row, 7, total_deviation_qty, format2)
                                sheet.write(row, 8, price, format2)
                                sheet.write(row, 9, updated_price, format2)
                                sheet.write(row, 10, total_deviation_price, format2)
                                sheet.write(row, 11, po_amount, format2)
                                sheet.write(row, 12, updated_po_amount, format2)
                                sheet.write(row, 13, total_deviation_amount, format2)
                                sheet.write(row, 14, history_create_date, format2)
                                sheet.write(row, 15, history_record, format2)
                                sheet.write(row, 16, reason, format2)

                                row = row + 1

                    if id.line_ids:
                        lines = []
                        for line in id.line_ids:
                            lines.append(line.product_id.id)
                        for revision_line in id.old_revision_ids[-1]:
                            original_po_name = revision_line.name   
                        purchase_order = self.env['purchase.requisition'].search([('name','=',original_po_name)])
                        updated_po_amount = 0
                        updated_quantity = 0
                        updated_price = 0
                        for po_order in purchase_order:
                            if po_order.line_ids:
                                for po_line in po_order.line_ids:
                                    if po_line.product_id.id not in lines:
                                        product = po_line.product_id.name
                                        quantity = po_line.product_qty
                                        price = po_line.price_unit
                                        po_amount  = po_line.price_total_base
                                        total_deviation_qty = updated_quantity - quantity
                                        total_deviation_price = updated_price - price
                                        total_deviation_amount = updated_po_amount - po_amount

                                        sheet.write(row, 0, name, format2)
                                        sheet.write(row, 1, id.name, format2)
                                        sheet.write(row, 2, product, format2)
                                        sheet.write(row, 3, username, format2)
                                        sheet.write(row, 4, currency, format2)
                                        sheet.write(row, 5, quantity, format2)
                                        sheet.write(row, 6, updated_quantity, format2)
                                        sheet.write(row, 7, total_deviation_qty, format2)
                                        sheet.write(row, 8, price, format2)
                                        sheet.write(row, 9, updated_price, format2)
                                        sheet.write(row, 10, total_deviation_price, format2)
                                        sheet.write(row, 11, po_amount, format2)
                                        sheet.write(row, 12, updated_po_amount, format2)
                                        sheet.write(row, 13, total_deviation_amount, format2)
                                        sheet.write(row, 14, history_create_date, format2)
                                        sheet.write(row, 15, history_record, format2)
                                        sheet.write(row, 16, reason, format2)

                                        row = row + 1
                                
            except:
                sheet.write(row,0,'There is No Revision Available',format1)
                row = row + 1
        workbook.close()