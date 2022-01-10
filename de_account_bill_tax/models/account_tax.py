# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = "account.tax"
    
    tax_category = fields.Selection(selection=[
        ('gst', 'GST'),
        ('wht', 'WHT'),
       ],
        string="Tax Category", default='gst', required=True)
