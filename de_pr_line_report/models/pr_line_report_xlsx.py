from odoo import models


class GenerateXLSXReport(models.Model):
    _name = 'report.de_pr_line_report.pr_line_report_xlsx'
    _description = 'Purchase Requisition Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines,model="ir.actions.report",output_format="xlsx",report_name="de_pr_line_report.pr_line_report_xlsx"):
        

        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Products Report')
        sheet.write(3, 0, 'PR No.', format1)
        sheet.write(3, 1, 'PR Date', format1)
        sheet.write(3, 2, 'PR Status', format1)
        sheet.write(3, 3, 'PR Line ID', format1)
        sheet.write(3, 4, 'Product', format1)
        sheet.write(3, 5, 'Product Category', format1)
        sheet.write(3, 6, 'Description', format1)
        sheet.write(3, 7, 'Cost Center', format1)
        sheet.write(3, 8, 'Site ID', format1)
        sheet.write(3, 9, 'Tenant', format1)
        sheet.write(3, 10, 'PR Line-quantity', format1)
        sheet.write(3, 11, 'UoM', format1)
        sheet.write(3, 12, 'Delivery Date', format1)
        sheet.write(3, 13, 'Unit Price', format1)
        sheet.write(3, 14, 'Subtotal Line Amount', format1)
        sheet.write(3, 15, 'Currency', format1)
        sheet.write(3, 16, 'PR Created by', format1)

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

        #purchase_ids = self.env['purchase.requisition'].browse(data['id'])
        
        for id in lines:
            if id.name:
                name = id.name
            else:
                name = None
            if id.state:
                state = id.state
            else:
                state = None
            
            
            if id.ordering_date:
                date = id.ordering_date
                ordering_date = date.strftime("%m/%d/%Y")
            else:
                ordering_date = None
            if id.schedule_date:
                sched_date = id.schedule_date
                delivery_date = sched_date.strftime("%m/%d/%Y")
            else:
                delivery_date = None
            if id.currency_id:
                currency = id.currency_id.name
            else:
                currency = None
            
            if id.user_id:
                user_id = id.user_id.name
            else:
                user_id = None
            try:
                if id.partner_id:
                    partner_id = id.partner_id.name
                else:
                    partner_id = None
            except:
                partner_id = None
            
            if id.line_ids:
                for line in id.line_ids:
                    if line.product_id:
                        product_id = id.product_id.name
                    else:
                        product_id = None
                    if line.product_id.categ_id:
                        category = line.product_id.categ_id.name
                    else:
                        category = None
                    if line.product_description_variants:
                        description = line.product_description_variants
                    else:
                        description = None
                    if line.analytic_tag_ids:
                        analytic_tag = line.analytic_tag_ids.name
                    else:
                        analytic_tag = None
                    try:
                        if line.project_id:
                            project_id = line.project_id.name
                        else:
                            project_id = None
                    except:
                        project_id = None
                    if line.product_qty:
                        qty = line.product_qty
                    else:
                        qty = None
                    if line.product_uom_id:
                        uom = line.product_uom_id.name
                    else:
                        uom = None
                    if line.price_unit:
                       price_unit = line.price_unit
                    else:
                        price_unit = None
                    if line.price_total_base:
                        subtotal = line.price_total_base
                    else:
                        subtotal = None
                        
                    sheet.write(row, 0, name, format2)
                    sheet.write(row, 1, ordering_date, format2)
                    sheet.write(row, 2, state, format2)
                    sheet.write(row, 3, line.id, format2)
                    sheet.write(row, 4, product_id, format2)
                    sheet.write(row, 5, category, format2)
                    sheet.write(row, 6, description, format2)
                    sheet.write(row, 7, analytic_tag, format2)
                    sheet.write(row, 8, project_id, format2)
                    sheet.write(row, 9, partner_id, format2)
                    sheet.write(row, 10, qty, format2)
                    sheet.write(row, 11, uom, format2)
                    sheet.write(row, 12, delivery_date, format2)
                    sheet.write(row, 13, price_unit, format2)
                    sheet.write(row, 14, subtotal, format2)
                    sheet.write(row, 15, currency, format2)
                    sheet.write(row, 16, user_id, format2)

                    row = row + 1
