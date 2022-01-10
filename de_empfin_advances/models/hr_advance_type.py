# -*- coding: utf-8 -*-

from odoo import fields, models, _


class HrAdvanceType(models.Model):
    _name = 'hr.advance.type'
    _description = 'Advance Type'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product', domain=[('type', '=', 'service')], change_default=True)

