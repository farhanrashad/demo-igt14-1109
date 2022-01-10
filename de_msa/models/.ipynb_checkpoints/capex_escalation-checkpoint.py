# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class capex_escalation(models.Model):
    _name = "capex.escalation"
    _description = 'CAPEX Escalation'
  
    year = fields.Char(string='Year', required=True, size=4)
    cpi = fields.Float(string='CPI')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')
