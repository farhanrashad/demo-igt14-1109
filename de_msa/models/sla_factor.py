# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _


class sla_factor(models.Model):
    _name = 'sla.factor'
    _description = 'SLA Factor'

    name = fields.Many2one('sla.factor.value', string='SLA Factor', required=True)
    factor = fields.Float(string='Factor')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')

    
    

class sla_factor_value(models.Model):
    _name = 'sla.factor.value'
    _description = 'SLA Factor Value'

    name = fields.Char(string='Name', required=True)
