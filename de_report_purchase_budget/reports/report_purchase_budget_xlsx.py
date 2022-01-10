# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError

from odoo.exceptions import UserError
import datetime
import calendar


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_purchase_budget.report_purchase_budget'
    _description = 'Purchase Budget Report XLSX'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines,model="ir.actions.report",output_format="xlsx",report_name="de_report_purchase_budget.report_purchase_budget"):
        
        format1 = workbook.add_format({'font_size': '10', 'align': 'center', 'bold': True, 'border':True, 'bg_color': '#ffffcc'})
        format2 = workbook.add_format({'font_size': '10', 'align': 'center', 'border':True,})
        format3 = workbook.add_format({'font_size': '10', 'align': 'right', 'num_format':'#,##0.00', 'border':True, 'italic':True})
        department = duration = month = ''  
        i = 1
        sheet_name = ''
        
        temp = ''
        po_lines = self.env['purchase.order.line']
        #budget_opening_lines = self.env['purchasse.budget.line']
        used_qty = used_amt = rem_qty = rem_amt = 0
        price = total = 0
        while i <= 13:
            if i == 1:
                sheet_name = 'JAN'
            elif i == 2:
                sheet_name = 'FEB'
            elif i == 3:
                sheet_name = 'MAR'
            elif i == 4:
                sheet_name = 'APR'
            elif i == 5:
                sheet_name = 'MAY'
            elif i == 6:
                sheet_name = 'JUN'
            elif i == 7:
                sheet_name = 'JUL'
            elif i == 8:
                sheet_name = 'AUG'
            elif i == 9:
                sheet_name = 'SEP'
            elif i == 10:
                sheet_name = 'OCT'
            elif i == 11:
                sheet_name = 'NOV'
            elif i == 12:
                sheet_name = 'DEC'
            elif i == 13:
                sheet_name = 'TOTAL'

            sheet = workbook.add_worksheet(str(sheet_name))
            #sheet.merge_range('A2:D2', 'Budget Line Report', format0)
        
            sheet.write(3, 0, 'Department', format1)
            sheet.write(3, 1, 'Budget Reference', format1)
            sheet.write(3, 2, 'Duration', format1)
            sheet.write(3, 3, 'Month', format1)
            sheet.write(3, 4, 'Category', format1)
            sheet.write(3, 5, 'Line Budget', format1)
            sheet.write(3, 6, 'Allocated QTY', format1)
            sheet.write(3, 7, 'Allocated Unit Price', format1)
            sheet.write(3, 8, 'Allocated Amount', format1)
            sheet.write(3, 9, 'Used QTY', format1)
            sheet.write(3, 10, 'Used Amount', format1)
            sheet.write(3, 11, 'Available QTY', format1)
            sheet.write(3, 12, 'Available Amount', format1)
            
            row = 4
            sheet.set_column(row, 0, 50)
            sheet.set_column(row, 1, 25)
            sheet.set_column(row, 2, 20)
            sheet.set_column(row, 3, 20)
            #sheet.set_column(row, 4, 20)
            sheet.set_column(row, 4, 20)
            sheet.set_column(row, 5, 20)
            sheet.set_column(row, 6, 20)
            sheet.set_column(row, 7, 20)
            sheet.set_column(row, 8, 20)
            sheet.set_column(row, 9, 20)
            sheet.set_column(row, 10, 20)
            sheet.set_column(row, 11, 20)
            sheet.set_column(row, 12, 20)
        
            for budget in lines:
                used_qty = used_amt = rem_qty = rem_amt = planned_qty = planned_amt = 0
                price = total = 0
                for dept in budget.department_ids:
                    department += dept.name + '-'
                month = str(budget.date_from.strftime("%d-%m-%Y"))
                if budget.purchase_budget_line:
                    for line in budget.purchase_budget_line:
                        used_qty = used_amt = rem_qty = rem_amt = 0
                        price = total = 0
                        temp = ''
                        po_lines = self.env['purchase.order.line'].search([('purchase_budget_line_id','=',line.id),('state','in',['purchase','done'])])
                        #budget_opening_lines = self.env['purchasse.budget.line'].search([('id','=',line.id),('budget_id.state','in',['validate','done'])])

                        duration = str(line.date_from.strftime("%d-%m-%Y")) + '-' + str(line.date_to.strftime("%d-%m-%Y"))
                        
                        
                        if i == 13:
                            used_qty = line.practical_quantity
                            used_amt = line.practical_amount
                            planned_qty = line.planned_quantity
                            planned_amt = line.planned_quantity * line.planned_price_unit
                        else:
                            
                            #planned_amt = line.planned_quantity * line.planned_price_unit
                            for pline in po_lines.filtered(lambda p: int(p.date_order.strftime("%m")) == i):
                                used_qty += pline.product_qty
                                if not (pline.currency_id.id == line.purchase_budget_id.currency_id.id):
                                    #total += pline.currency_id._get_conversion_rate(pline.currency_id, budget.currency_id,budget.company_id, fields.date.today()) * pline.price_subtotal
                                    total += pline.currency_id._convert(pline.price_subtotal, line.purchase_budget_id.currency_id, line.purchase_budget_id.company_id, fields.date.today()) 

                                else:
                                    total += pline.price_subtotal
                                used_amt = total
                                #temp += str(pline.order_id.name) + ' - qty=' + str(pline.product_qty) + '/price=' + str(total) + '/docprice=' + str(pline.price_unit) + '\n'
                            #planned_qty = 0  
                            used_qty1 = 0
                            used_amt1 = 0
                            ototal = 0
                            for oline in po_lines.filtered(lambda p: int(p.date_order.strftime("%m")) < i):
                                used_qty1 += oline.product_qty
                                if not (oline.currency_id.id == line.purchase_budget_id.currency_id.id):
                                    ototal += oline.currency_id._convert(oline.price_subtotal, line.purchase_budget_id.currency_id, line.purchase_budget_id.company_id, fields.date.today()) 
                                else:
                                    ototal += oline.price_subtotal
                                used_amt1 = ototal
                                
                            planned_qty = line.planned_quantity - used_qty1
                            planned_amt = line.planned_amount - used_amt1
                        rem_qty = planned_qty - used_qty
                        rem_amt = planned_amt - used_amt
                        
                        
                        
                        sheet.write(row, 0, department, format2)
                        sheet.write(row, 1, budget.name, format2)
                        sheet.write(row, 2, duration, format2)
                        sheet.write(row, 3, sheet_name, format2)
                        sheet.write(row, 4, line.exp_category_id.complete_name, format2)
                        #sheet.write(row, 4, line.expense_category, format2)
                        sheet.write(row, 5, line.name, format2)
                        sheet.write(row, 6, planned_qty, format2)
                        sheet.write(row, 7, line.planned_price_unit, format3)
                        sheet.write(row, 8, planned_amt, format3)
                        sheet.write(row, 9, used_qty, format2)
                        sheet.write(row, 10, used_amt, format3)
                        #sheet.write(row, 10, temp, format2)
                        sheet.write(row, 11, rem_qty, format2)
                        sheet.write(row, 12, rem_amt, format3)

                        row = row + 1
                        
            i += 1
                    