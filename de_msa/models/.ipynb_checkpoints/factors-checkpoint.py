# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class location_factor(models.Model):
    _name = "location.factor"
    _description = 'Location Factor'
    
    state_id = fields.Many2one('res.country.state', string='Region', domain="[('country_id.name', '=', 'Myanmar')]", required=True)
    factor = fields.Float(string='Factor', digits=(16, 4))
    region_number = fields.Integer(string='Region Number')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')

#Wind Factor    
class wind_factor(models.Model):
    _name = 'wind.factor'
    _description = 'Wind Factor'

    name = fields.Many2one('wind.factor.value', string='Wind Factor Value', required=True)
    factor = fields.Float(string='Factor', digits=(16, 4))
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')

    
class wind_factor_value(models.Model):
    _name = 'wind.factor.value'
    _description = 'Wind Factor Value'

    name = fields.Char(string='Name', required=True)
    
    
#SLA Factor
class sla_factor(models.Model):
    _name = 'sla.factor'
    _description = 'SLA Factor'

    name = fields.Many2one('sla.factor.value', string='SLA Factor', required=True)
    factor = fields.Float(string='Factor', digits=(16, 4))
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')

class sla_factor_value(models.Model):
    _name = 'sla.factor.value'
    _description = 'SLA Factor Value'

    name = fields.Char(string='Name', required=True)
