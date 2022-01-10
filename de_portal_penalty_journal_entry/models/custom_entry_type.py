# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CustumEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    penalty_published = fields.Boolean(string='publish penalty on website')
    
    
    
       
