# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class msa_penalty(models.Model):
    _name = "msa.penalty"
    _description = 'MSA Penalty'
    
    
    name = fields.Char(string='Name', required=True)
    penalties = fields.Float(string='Penalties (%)')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')