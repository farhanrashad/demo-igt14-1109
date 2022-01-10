# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError

from odoo.exceptions import UserError
import datetime
import calendar


class GenerateXLSXReport(models.Model):
    _name = 'report.de_report_purchase_budget_sum.report_purchase_budget'
    _description = 'Purchase Budget Report XLSX'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines,model="ir.actions.report",output_format="xlsx",report_name="de_report_purchase_budget_sum.report_purchase_budget"):
        
        format0 = workbook.add_format({'font_size': '16', 'align': 'center', 'bold': True, })
        format1 = workbook.add_format({'font_size': '10', 'align': 'center', 'bold': True, 'border':True, 'bg_color': '#ffffcc'})
        format2 = workbook.add_format({'font_size': '10', 'align': 'center', 'border':True,})
        format3 = workbook.add_format({'font_size': '10', 'align': 'right', 'num_format':'#,##0.00', 'border':True, 'italic':True})
        
        sheet = workbook.add_worksheet('Category')
        sheet.merge_range('A2:D2', 'Budget Line Summary Report', format0)
        #sheet.write(1, 4, 'Budget Line Summary Report', format0)
       
        
        #sheet = workbook.add_worksheet("Category")
        sheet.write(4, 0, 'Category', format1)
        sheet.write(4, 1, 'Budget Allocated Amount', format1)
        sheet.write(4, 2, 'Total Issued PO', format1)
        sheet.write(4, 3, 'Remaining Amount', format1)
           
        row = 5
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
            
        cat_list = []
        for budget in lines.purchase_budget_line:
            if budget.exp_category_id not in cat_list:
                cat_list.append(budget.exp_category_id)
        planned_amount = actual_amount = 0.0
        for cat in cat_list:
            planned_amount = actual_amount = 0.0
            sheet.write(row, 0, cat.complete_name, format2)
            for line in lines.purchase_budget_line.filtered(lambda x: x.exp_category_id.id == cat.id):
                planned_amount += line.planned_amount
                actual_amount += line.practical_amount
            sheet.write(row, 1, planned_amount, format3)
            sheet.write(row, 2, actual_amount, format3)
            sheet.write(row, 3, (planned_amount - actual_amount), format3)
            row = row + 1
            
        
        #Department Budget Summary
        sheet = workbook.add_worksheet('Departmental')
        sheet.merge_range('A2:D2', 'Budget Line Summary Report', format0)
        #sheet.write(1, 4, 'Budget Line Summary Report', format0)
       
        
        #sheet = workbook.add_worksheet("Category")
        sheet.write(4, 0, 'Department', format1)
        sheet.write(4, 1, 'Budget Allocated Amount', format1)
        sheet.write(4, 2, 'Total Issued PO', format1)
        sheet.write(4, 3, 'Remaining Amount', format1)
           
        row = 5
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
            
        dept_list = []
        for dept in lines.department_ids:
            if dept not in dept_list:
                dept_list.append(dept)
        planned_amount = actual_amount = 0.0
        for dept in dept_list:
            planned_amount = actual_amount = 0.0
            sheet.write(row, 0, dept.name, format2)
            for budget in lines:
                if dept in budget.department_ids:
                    for line in budget.purchase_budget_line:
                        planned_amount += line.planned_amount
                        actual_amount += line.practical_amount
            sheet.write(row, 1, planned_amount, format3)
            sheet.write(row, 2, actual_amount, format3)
            sheet.write(row, 3, (planned_amount - actual_amount), format3)
            row = row + 1