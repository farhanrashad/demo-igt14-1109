# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    hr_expense_sheet_type_id  = fields.Many2one('hr.expense.sheet.type', string='Expense Type')
    expense_type_id = fields.Many2one('hr.expense.type', string='Expense Category', copy=False)
    
    