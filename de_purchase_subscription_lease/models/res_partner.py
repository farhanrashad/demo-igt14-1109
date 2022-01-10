# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    bank_key_contact = fields.Char(string='Bank Key Contact')
    