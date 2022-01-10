# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class site_load(models.Model):
    _name = 'site.load'
    _description = 'Site Load'

    power_type = fields.Many2one('product.product', string='Power Model', domain="[('sale_ok', '=', True),('is_product_category_power', '=', True)]", required=True)
    msa_id = fields.Many2one('master.service.agreement', string='MSA')
    access_low = fields.Float(string='Access Low')
    access_high = fields.Float(string='Access High')
    dwdm = fields.Float(string='DWDM')
    standard_hub = fields.Float(string='Standard Hub')
