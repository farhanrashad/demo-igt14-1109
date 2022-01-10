# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class power_prices(models.Model):
    _name = 'power.prices'
    _description = 'Power Prices'
    
    power_type = fields.Many2one('product.product', string='Power Model', domain="[('sale_ok', '=', True), ('is_product_category_power', '=', True)]", required=True)
    ip_fee_capex = fields.Float(string='IP Fee Power CAPEX')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')