# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class opex_cpi(models.Model):
    _name = "opex.cpi"
    _description = 'OPEX CPI'
    
    year = fields.Char(string='Year', required=True, size=4)
    cpi = fields.Float(string='CPI', digits=(16, 4))
    msa_id =fields.Many2one('master.service.agreement', string='Master Service Agreement')
    cpio = fields.Float(string='Ooredoo CPI rate', digits=(16, 4))