# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _


class target_pass_through(models.Model):
    _name = 'target.pass.through'
    _description = 'Target Pass Through'
    
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')
    power_model_id = fields.Many2one('product.product', string='Power Model', domain="[('sale_ok', '=', True), ('is_product_category_power', '=', True)]")
    site_load = fields.Selection([('access_low', 'Access Low'),
                                  ('access_hight', 'Access High'),
                                  ('dwdm', 'DWDM'),
                                  ('standard_hub', 'Standard Hub')],
                                 string='Site Load', default='access_low')
    target_fuel_consumption = fields.Float(string='Target Fuel Consumption')
    target_eb_consumption = fields.Float(string='Target EB Consumption')
