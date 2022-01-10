# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    oem_serial_no = fields.Char(string='OEM Serial No', store=True, readonly=False)