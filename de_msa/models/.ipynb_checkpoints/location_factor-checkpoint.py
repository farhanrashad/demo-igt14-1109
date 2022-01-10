# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class location_factor(models.Model):
    _name = "location.factor"
    _description = 'Location Factor'
    
    state_id = fields.Many2one('res.country.state', string='Region', domain="[('country_id.name', '=', 'Myanmar')]", required=True)
    factor = fields.Float(string='Factor', digits=(16, 3))
    region_number = fields.Integer(string='Region Number')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')
