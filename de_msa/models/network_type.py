# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _


class network_type(models.Model):
    _name = 'network.type'
    _description = 'Network Type'
    name = fields.Char(string='Name')
