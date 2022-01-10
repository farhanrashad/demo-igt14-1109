# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class tower_without_power(models.Model):
    _name = 'tower.without.power'
    _description = 'Tower Without Power'
    
    tower_type = fields.Many2one('product.product', string='Tower Type', domain="[('sale_ok', '=', True),('is_product_category_tower', '=', True)]", required=True)
    ip_fee_capex = fields.Float(string='IP Fee For CAPEX')
    ip_fee_opex = fields.Float(string='IP Fee For OPEX')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')
    