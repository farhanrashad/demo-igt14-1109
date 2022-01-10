# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CustumEntry(models.Model):
    _inherit = 'account.custom.entry'
    
       
class CustumEntryline(models.Model):
    _inherit = 'account.custom.entry.line'
    

class CustumEntrystage(models.Model):
    _inherit = 'account.custom.entry.stage'    